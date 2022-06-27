from functools import singledispatch
from itertools import chain
from typing import List, Optional
from collections import OrderedDict, abc
from operator import add
import re

from .config import Config
from .parser import ConfigParser
from .snippet import ConfigSnippet
from .types import ConfigFile, WILDCARD, ConfigName, ConfigChainOptions
from .utils import dict_merge_with_wildcard, merge_profile_with_wildcard


def auto_filler(config_name_statement, loader):
    # set default name for configs in the one file
    the_first_config_snippet = list(loader.values())[0][0]
    global_default_name = get_config_name(
        config_name_statement, the_first_config_snippet
    )
    _a, _b, global_default_name_dict = get_config_name_dict(
        config_name_statement, the_first_config_snippet
    )
    for configs_in_onefile in loader.values():
        auto_fill_configs_name(
            configs_in_onefile,
            config_name_statement,
            global_default_name,
            global_default_name_dict,
        )


def auto_fill_configs_name(
    configs_in_onefile, config_name_statement, default_name, default_name_dict
):
    if len(configs_in_onefile) == 0:
        return

    names = [
        get_config_name(config_name_statement, config) for config in configs_in_onefile
    ]
    if names[0] != "*":
        _, _, d = get_config_name_dict(config_name_statement, configs_in_onefile[0])
        [other.update(d) for other in configs_in_onefile[1:]]
    else:
        if default_name != "*":
            [other.update(default_name_dict) for other in configs_in_onefile]


class ConfigSet(OrderedDict):
    @classmethod
    def load(cls, *args: ConfigFile, **kwargs: ConfigChainOptions) -> "ConfigSet":
        loader = ConfigParser(*args, **kwargs)
        loader.load()

        config_name_statement = kwargs.get("name", WILDCARD)

        auto_filler(config_name_statement, loader)

        named_snippets = OrderedDict()
        for snippet in chain(*loader.values()):
            named_snippets.setdefault(
                get_config_name(config_name_statement, snippet), [],
            ).append(snippet)

        named_configs = {
            name: Config.from_snippets(snippets, **kwargs)
            for name, snippets in named_snippets.items()
        }

        merge_profile_with_wildcard(named_configs)
        return cls(named_configs)

    def __add__(self, other: "ConfigSet") -> "ConfigSet":
        return dict_merge_with_wildcard(self, other, add)

    def config_names(self) -> List[ConfigName]:
        return self.keys()


@singledispatch
def get_config_name(_getter, _snippet: ConfigSnippet) -> ConfigName:
    return WILDCARD


@get_config_name.register
def _(config_name_getter: abc.Callable, snippet: ConfigSnippet) -> ConfigName:
    return config_name_getter(snippet)


def get_config_name_dict(config_name_statement, snippet):
    reg = r"\${(\w+)}"
    matches = re.findall(reg, config_name_statement)
    vars = {v: snippet.find(v) for v in matches}
    return matches, reg, vars


@get_config_name.register
def _(config_name_statement: str, snippet: ConfigSnippet) -> ConfigName:
    matches, reg, vars = get_config_name_dict(config_name_statement, snippet)
    if (
        len(matches) > 0
        and len(
            [
                exist
                for exist in [vars.get(m, None) for m in matches]
                if exist is not None
            ]
        )
        == 0
    ):
        return WILDCARD

    def sub(var):
        (key,) = var.groups()
        return str(vars.get(key, None))

    return re.sub(reg, sub, config_name_statement)


@get_config_name.register
def _(config_name_keys: abc.MutableSequence, snippet: ConfigSnippet) -> ConfigName:
    ids = [
        str(n) for n in [snippet.find(key) for key in config_name_keys] if n is not None
    ]
    if ids:
        return "-".join(ids)
    else:
        return WILDCARD

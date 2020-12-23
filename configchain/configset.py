from itertools import chain
from typing import List, Optional, Any, Union
from collections import OrderedDict
from operator import add
import re

from .config import Config
from .loader import ConfigLoader
from .snippet import ConfigSnippet
from .types import ConfigKey, ConfigFile, WILDCARD, ConfigName, ConfigNameGetter
from .utils import dict_merge_with_wildcard


class ConfigSet(OrderedDict):
    @classmethod
    def load(cls, *args: ConfigFile, **kwargs: Any) -> "ConfigSet":
        loader = ConfigLoader(*args, **kwargs)
        loader.load()

        named_snippets = OrderedDict()
        for snippet in chain(*loader.values()):
            named_snippets.setdefault(
                get_config_name(kwargs.get("name", "${group}-${name}"), snippet), [],
            ).append(snippet)

        named_configs = {
            name: Config.from_snippets(snippets, **kwargs)
            for name, snippets in named_snippets.items()
        }
        return cls(named_configs)

    def __add__(self, other: "ConfigSet") -> "ConfigSet":
        return dict_merge_with_wildcard(self, other, add)

    def config_names(self) -> List[ConfigName]:
        return self.keys()

    def get_config(
        self, key: ConfigName, default: Optional[Config] = None
    ) -> Optional[Config]:
        return self.get(key, default)


def get_config_name_by_fields(
    from_fields: List[ConfigKey], snippet: ConfigSnippet
) -> ConfigName:
    ids = [
        str(n) for n in [snippet.find(field) for field in from_fields] if n is not None
    ]
    if ids:
        return "-".join(ids)
    else:
        return WILDCARD


def get_config_name_by_statement(getter: str, snippet: ConfigSnippet):
    reg = r"\${(\w+)}"
    matches = re.findall(reg, getter)
    vars = {v: snippet.find(v) for v in matches}
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

    return re.sub(reg, sub, getter)


def get_config_name(
    getter: Union[str, ConfigNameGetter], snippet: ConfigSnippet
) -> ConfigName:
    if callable(getter):
        return getter(snippet)
    if isinstance(getter, str):
        return get_config_name_by_statement(getter, snippet)
    if isinstance(getter, list):
        return get_config_name_by_fields(getter, snippet)
    return WILDCARD

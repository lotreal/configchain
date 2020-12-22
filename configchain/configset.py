from collections import OrderedDict
from operator import add
from typing import List, Optional, Any

from .config import Config
from .loader import ConfigLoader
from .snippet import ConfigSnippet
from .types import ConfigKey, ConfigFile, PROFILE_GLOBAL, ConfigName
from .utils import list_flatten, dict_merge_with_wildcard


class ConfigSet(OrderedDict):
    @classmethod
    def load(cls, *args: ConfigFile, **kwargs: Any) -> "ConfigSet":
        loader = ConfigLoader(*args, **kwargs)
        loader.load()

        name_getter = kwargs.get("name_getter", ["group", "name"])

        snippets = list_flatten(loader.values())

        def name(snippet: ConfigSnippet, from_fields: List[ConfigKey]) -> str:
            ids = [
                n
                for n in [snippet.find(field) for field in from_fields]
                if n is not None
            ]
            if ids:
                return "-".join(ids)
            else:
                return PROFILE_GLOBAL

        named_snippets = dict()
        for snippet in snippets:
            named_snippets.setdefault(name(snippet, name_getter), []).append(
                snippet
            )

        named_configs = {
            name: Config.from_snippets(snippets)
            for name, snippets in named_snippets.items()
        }
        return cls(named_configs)

    def get(self, key: ConfigName, default: Optional[Config] = None) -> Optional[Config]:
        return OrderedDict.get(self, key, default)

    def __add__(self, other: "ConfigSet") -> "ConfigSet":
        return dict_merge_with_wildcard(self, other, add)

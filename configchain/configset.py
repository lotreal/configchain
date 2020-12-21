from collections import OrderedDict
from operator import add
from typing import List, Optional

from .config import Config
from .loader import ConfigLoader
from .snippet import ConfigSnippet
from .types import KT
from .utils import list_flatten, dict_merge


class ConfigSet(OrderedDict):
    @classmethod
    def load(cls, *args, **kwargs) -> "ConfigSet":
        loader = ConfigLoader(*args, **kwargs)
        loader.load()

        snippets = list_flatten(loader.values())

        def name(snippet: ConfigSnippet, from_fields: List[str]):
            ids = [
                n
                for n in [snippet.find(field) for field in from_fields]
                if n is not None
            ]
            if ids:
                return "-".join(ids)
            else:
                return "*"

        named_snippets = dict()
        for snippet in snippets:
            named_snippets.setdefault(name(snippet, ["group", "name"]), []).append(
                snippet
            )

        named_configs = {
            name: Config.from_snippets(snippets)
            for name, snippets in named_snippets.items()
        }
        return cls(named_configs)

    def get(self, key: KT, default: Optional[Config]=None) -> Optional[Config]:
        return OrderedDict.get(self, key, default)

    def __add__(self, other):
        m = dict_merge(self, other, add)
        g = m.get("*", None)
        if g is not None:
            for k, v in m.items():
                if k == "*":
                    continue
                m[k] = g + m[k]
        return m
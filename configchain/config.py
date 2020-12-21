from collections import OrderedDict
from functools import reduce
from operator import add
from typing import List, Dict, Optional

from .snippet import ConfigSnippet
from .types import PROFILE_GLOBAL, ProfileKey, KT
from .utils import list_groupby, dict_merge


class Config(OrderedDict):
    name: str

    @classmethod
    def from_snippets(cls, snippets: List[ConfigSnippet]) -> "Config":
        def groupby_profile_and_merge(
            snippets: List[ConfigSnippet],
        ) -> List[ConfigSnippet]:
            return [reduce(add, g) for g in list_groupby(snippets, lambda s: s.profile)]

        gs = groupby_profile_and_merge(snippets)
        config = OrderedDict()
        for snippet in gs:
            config.setdefault(snippet.profile, snippet)

        global_profile = config.pop(PROFILE_GLOBAL, None)
        if global_profile is not None:
            config = {p: global_profile + c for p, c in config.items()}
            config.update({PROFILE_GLOBAL: global_profile})

        return Config(config)

    def get(self, key: KT, default: Optional[ConfigSnippet] = None) -> Optional[ConfigSnippet]:
        return OrderedDict.get(self, key, default)

    def __add__(self, other: "Config") -> "Config":
        m = dict_merge(self, other, add)
        g = m.get("*", None)
        if g is not None:
            for k, v in m.items():
                if k == "*":
                    continue
                m[k] = g + m[k]
        return m

from collections import OrderedDict
from functools import reduce
from operator import add
from typing import List, Optional

from .snippet import ConfigSnippet
from .types import PROFILE_GLOBAL, ProfileKey
from .utils import list_groupby, dict_merge_with_wildcard


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

    def get(
        self, key: ProfileKey, default: Optional[ConfigSnippet] = None
    ) -> Optional[ConfigSnippet]:
        return super().get(key, default)

    def profile(self, key: ProfileKey) -> Optional[ConfigSnippet]:
        return self.get(key, self.get(PROFILE_GLOBAL))

    def __add__(self, other: "Config") -> "Config":
        return dict_merge_with_wildcard(self, other, add)

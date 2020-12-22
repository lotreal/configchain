from collections import OrderedDict
from functools import reduce
from operator import add
from typing import List, Optional

from .snippet import ConfigSnippet
from .types import PROFILE_WILDCARD, ProfileKey
from .utils import list_groupby, dict_merge_with_wildcard


class Config(OrderedDict):
    name: str

    @classmethod
    def from_snippets(cls, snippets: List[ConfigSnippet]) -> "Config":
        def groupby_profile_and_merge(
            snippets: List[ConfigSnippet],
        ) -> List[ConfigSnippet]:
            return [reduce(add, g) for g in list_groupby(snippets, lambda s: s.profile)]

        profile_snippets = groupby_profile_and_merge(snippets)
        config = OrderedDict({s.profile: s for s in profile_snippets})

        wp = config.get(PROFILE_WILDCARD, None)
        if wp is not None:
            config.update({p: wp + c for p, c in config.items() if p != PROFILE_WILDCARD})

        return Config(config)

    def get(
        self, key: ProfileKey, default: Optional[ConfigSnippet] = None
    ) -> Optional[ConfigSnippet]:
        return super().get(key, default)

    def profile(self, key: ProfileKey) -> Optional[ConfigSnippet]:
        return self.get(key, self.get(PROFILE_WILDCARD))

    def __add__(self, other: "Config") -> "Config":
        return dict_merge_with_wildcard(self, other, add)

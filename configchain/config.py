from collections import OrderedDict
from functools import reduce
from operator import add
from typing import List, Optional, Callable

from .snippet import ConfigSnippet
from .types import PROFILE_WILDCARD, ProfileKey, ProfileName, PROFILE_NAME_KEY
from .utils import list_groupby, dict_merge_with_wildcard


class Config(OrderedDict):
    @classmethod
    def from_snippets(
        cls, snippets: List[ConfigSnippet], profile_key: ProfileKey = PROFILE_NAME_KEY
    ) -> "Config":
        profile_getter: Callable[["ConfigSnippet"], ProfileName] = lambda x: x.get(
            profile_key, PROFILE_WILDCARD
        )

        def groupby_profile_and_merge(
            snippets: List[ConfigSnippet],
        ) -> List[ConfigSnippet]:
            return [reduce(add, g) for g in list_groupby(snippets, profile_getter)]

        profile_snippets = groupby_profile_and_merge(snippets)
        config = OrderedDict({profile_getter(s): s for s in profile_snippets})

        wp = config.get(PROFILE_WILDCARD, None)
        if wp is not None:
            config.update(
                {p: wp + c for p, c in config.items() if p != PROFILE_WILDCARD}
            )

        return Config(config)

    def get(
        self, key: ProfileKey, default: Optional[ConfigSnippet] = None
    ) -> Optional[ConfigSnippet]:
        return super().get(key, default)

    def profile(self, key: ProfileKey) -> Optional[ConfigSnippet]:
        return self.get(key, self.get(PROFILE_WILDCARD))

    def __add__(self, other: "Config") -> "Config":
        return dict_merge_with_wildcard(self, other, add)

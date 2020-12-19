from functools import reduce
from operator import add
from typing import List, Dict

from configchain.snippet import ConfigSnippet
from configchain.types import PROFILE_GLOBAL, ProfileKey
from configchain.utils import list_groupby, dict_merge


class Config(dict):
    name: str

    @classmethod
    def from_snippets(cls, snippets: List[ConfigSnippet]) -> "Config":
        def groupby_profile_and_merge(
            snippets: List[ConfigSnippet],
        ) -> List[ConfigSnippet]:
            return [reduce(add, g) for g in list_groupby(snippets, lambda s: s.profile)]

        profiles: Dict[ProfileKey, ConfigSnippet] = {
            s.profile: s for s in groupby_profile_and_merge(snippets)
        }
        global_profile = profiles.pop(PROFILE_GLOBAL, None)
        if global_profile is not None:
            profiles = { p: global_profile + c for p, c in profiles.items()}
            profiles.update({PROFILE_GLOBAL: global_profile})

        config = cls(profiles)
        config.name = global_profile.config.get("name")
        return config

    def __add__(self, other: "Config") -> "Config":
        return dict_merge(self, other, add)
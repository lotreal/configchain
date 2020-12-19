from dataclasses import dataclass
from functools import reduce
from typing import List, Dict, Mapping

from configchain.snippet import ConfigSnippet, PROFILE_GLOBAL
from configchain.utils import list_groupby


@dataclass
class Config:
    name: str
    snippets: List[ConfigSnippet]
    # profiles: Mapping[str, Profile]

    # def get(self, profile: str) -> Profile:
    #     snippet = self.profiles.get(profile, self.profiles.get(PROFILE_GLOBAL))
    #     snippet_built = snippet.build()
    #     # snippet_built.sources.index = f"{self.name}-{snippet_built.sources.index}"
    #     return snippet_built

    @classmethod
    def from_snippets(cls, name: str, snippets: List[ConfigSnippet]) -> "Config":
        def link(b: ConfigSnippet, p: ConfigSnippet) -> ConfigSnippet:
            return p.extend(b)

        def groupby_profile_and_merge(
                snippets: List[ConfigSnippet],
        ) -> List[ConfigSnippet]:
            print(list_groupby(snippets, lambda s: s.profile))
            return 1
            return [
                (link, g) for g in list_groupby(snippets, lambda s: s.profile)
            ]

        def link_profiles_to_global(
                profile_snippet_mapping: Dict[str, ConfigSnippet],
                global_profile: ConfigSnippet,
        ) -> Dict[str, ConfigSnippet]:
            if global_profile is None:
                return profile_snippet_mapping

            for k, v in profile_snippet_mapping.items():
                if k != PROFILE_GLOBAL:
                    profile_snippet_mapping[k].extend(global_profile)
            return profile_snippet_mapping

        print(groupby_profile_and_merge(snippets))
        profile_snippet_mapping = {
            s.profile: s for s in groupby_profile_and_merge(snippets)
        }
        global_profile = profile_snippet_mapping.setdefault(PROFILE_GLOBAL, None)
        return cls(
            name=name,
            snippets=snippets,
            profiles=link_profiles_to_global(profile_snippet_mapping, global_profile),
        )

    def __len__(self) -> int:
        return len(self.profiles)

    def __add__(self, other: "Config") -> "Config":
        snippets = [s.clone() for s in self.snippets] + [
            s.clone() for s in other.snippets
        ]
        return Config.from_snippets(name=self.name, snippets=snippets)

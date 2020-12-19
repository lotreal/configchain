from dataclasses import dataclass
from typing import List, Dict, Optional, TypeVar, Any
from functools import reduce

from .source import ConfigSource
from .utils import dict_merge, config_merger

KT = TypeVar("KT")
VT = TypeVar("VT")


@dataclass(frozen=True)
class ConfigSnippet:
    config: Dict[str, Any]
    source: ConfigSource

    def get(self, k: KT, v: Optional[VT] = None) -> VT:
        return self.config.get(k, v)

    @property
    def profile(self, profile_key="profile", default_profile="*"):
        return self.config.get(profile_key, default_profile)

    def __repr__(self):
        return self.profile + ConfigSnippet.__repr__(self)


@dataclass
class ChainedConfigSnippet:
    nodes: List[ConfigSnippet]

    def build(self) -> "ConfigSnippet":
        def merge_snippet(b: ConfigSnippet, p: ConfigSnippet) -> ConfigSnippet:
            items = dict_merge(b.config, p.config, config_merger)
            source = b.source + p.source
            return ConfigSnippet(
                config=items, source=source
            )

        snippet_built = reduce(merge_snippet, self.nodes)
        return snippet_built

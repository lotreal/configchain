from dataclasses import dataclass, field
from typing import List, Dict, Optional, TypeVar, Any, Callable
from functools import reduce

from .source import ConfigSource
from .utils import dict_merge, config_merger

KT = TypeVar("KT")
VT = TypeVar("VT")


@dataclass(frozen=True)
class ConfigSnippet:
    config: Dict[str, Any]
    source: ConfigSource

    profile_getter: Callable[["ConfigSnippet"], str] = field(
        default=lambda x: x.config.get("profile", "*"),
        repr=False
    )

    def get(self, k: KT, v: Optional[VT] = None) -> VT:
        return self.config.get(k, v)

    @property
    def profile(self):
        return self.profile_getter(self)

    def __add__(self, other: "ConfigSnippet"):
        return ConfigSnippet(
            config=dict_merge(self.config, other.config, config_merger),
            source=self.source + other.source,
        )

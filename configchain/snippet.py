from collections import OrderedDict
from copy import copy, deepcopy
from typing import Dict, Any, Callable

from .source import ConfigSource
from .types import PROFILE_GLOBAL
from .utils import dict_merge, config_merger


class ConfigSnippet(OrderedDict):
    def __init__(self, config: Dict[str, Any], source: ConfigSource):
        super().__init__(config)
        self.source = source

    @property
    def profile(
        self,
        getter: Callable[["ConfigSnippet"], str] = lambda x: x.get(
            "profile", PROFILE_GLOBAL
        ),
    ):
        return getter(self)

    def __add__(self, other: "ConfigSnippet"):
        if other is None:
            return copy(self)

        return ConfigSnippet(
            config=dict_merge(self, other, config_merger),
            source=self.source + other.source,
        )

    def __copy__(self):
        return ConfigSnippet(
            config={k: copy(v) for k, v in self.items()}, source=self.source
        )

    def __deepcopy__(self, memodict={}):
        return ConfigSnippet(
            config={k: deepcopy(v, memodict) for k, v in self.items()},
            source=self.source,
        )

    def find(self, key):
        return self.get(key, self.source.find(key))

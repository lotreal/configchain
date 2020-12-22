from collections import OrderedDict
from copy import copy, deepcopy
from typing import Dict, Any, Callable

from .source import ConfigSource
from .utils import dict_merge, config_merger


class ConfigSnippet(OrderedDict):
    def __init__(self, config: Dict[str, Any], source: ConfigSource):
        super().__init__(config)
        self.source = source

    profile_getter: Callable[["ConfigSnippet"], str] = lambda x: x.get("profile", "*")

    @property
    def profile(self):
        return self.profile_getter()

    def __add__(self, other: "ConfigSnippet"):
        return ConfigSnippet(
            config=dict_merge(self, other, config_merger),
            source=self.source + other.source,
        )

    def __copy__(self):
        return ConfigSnippet(config={k: copy(v) for k, v in self.items()}, source=self.source)

    def __deepcopy__(self, memodict={}):
        return ConfigSnippet(config={k: deepcopy(v, memodict) for k, v in self.items()}, source=self.source)

    def find(self, key):
        return self.get(key, self.source.find(key))

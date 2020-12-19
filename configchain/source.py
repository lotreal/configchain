from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple, Union


@dataclass(frozen=True)
class ConfigSource:
    uri: str
    index: str

    @property
    def name(self):
        return self.uri

    def __str__(self) -> str:
        return f"{self.uri}:{self.index}"

    def __add__(
            self, other: "ConfigSource"
    ) -> "MergedConfigSource":
        return MergedConfigSource(sources=[self, other])


@dataclass(frozen=True)
class MergedConfigSource:
    sources: List[ConfigSource]

    def __add__(
            self, other: Union[ConfigSource, "MergedConfigSource"]
    ) -> "MergedConfigSource":
        sources = deepcopy(self.sources)
        if isinstance(other, ConfigSource):
            sources.append(other)
        if isinstance(other, MergedConfigSource):
            sources.extend(other.sources)
        return MergedConfigSource(sources=sources)

    def __str__(self) -> str:
        def create_breadcrumb(
                a: Tuple[str, str], s: ConfigSource
        ) -> Tuple[str, str]:
            name, breadcrumb = a
            if (n := s.name) == name:
                return n, f"{breadcrumb}-{s.index}"
            else:
                return n, f"{breadcrumb}-{n}-{s.index}"

        return reduce(create_breadcrumb, self.sources, ("", ""))[1].lstrip("-")

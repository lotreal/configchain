from copy import deepcopy
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Tuple, Union

from configchain.utils import list_uniq


@dataclass(frozen=True)
class ConfigSource:
    uri: str
    index: str
    loader: "ConfigLoader" = field(repr=False, default=None, hash=False)

    @property
    def name(self):
        return self.uri

    # def __hash__(self):
    #     return hash(str(self))

    def __str__(self) -> str:
        return f"{self.uri}:{self.index}"

    def __add__(self, other: "ConfigSource") -> "MergedConfigSource":
        return MergedConfigSource(sources=list([ self ])) + other

    def find(self, key):
        return self.loader.find(self.uri, key)
        if isinstance(self.source, MergedConfigSource):
            for loader, uri in reversed(
                [(s.loader, s.uri) for s in self.source.sources]
            ):
                v = self.find_from_loader(loader, uri, key)
                if v is not None:
                    return v
        return None


@dataclass(frozen=True)
class MergedConfigSource:
    sources: List[ConfigSource]

    def __add__(
        self, other: Union[ConfigSource, "MergedConfigSource"]
    ) -> "MergedConfigSource":
        if isinstance(other, ConfigSource):
            source = list([ other ])
        if isinstance(other, MergedConfigSource):
            source = other.sources
        return MergedConfigSource(sources=list_uniq(self.sources + source))

    def __str__(self) -> str:
        def create_breadcrumb(a: Tuple[str, str], s: ConfigSource) -> Tuple[str, str]:
            name, breadcrumb = a
            if (n := s.name) == name:
                return n, f"{breadcrumb}-{s.index}"
            else:
                return n, f"{breadcrumb}-{n}-{s.index}"

        return reduce(create_breadcrumb, self.sources, ("", ""))[1].lstrip("-")

    def find(self, key):
        for loader, uri in reversed(
            [(s.loader, s.uri) for s in self.sources]
        ):
            v = loader.find(uri, key)
            if v is not None:
                return v
        return None

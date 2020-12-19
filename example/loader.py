from configchain.config import Config
from configchain.loader import ConfigLoader
from configchain.snippet import ConfigSnippet, ProfileSnippet
from configchain.source import ConfigSource
from configchain.utils import list_flatten

loader = ConfigLoader("./test/asset/api.yaml")
loader.load()


def gs(conf: dict, file: str, index, dicts: list) -> ConfigSnippet:
    print(id(dicts))
    return ProfileSnippet(
        config=conf, source=ConfigSource(index=index, file=file, raw=dicts)
    )


snippets = list_flatten([
    [gs(d, file, index, dicts) for index, d in enumerate(dicts)]
    for file, dicts in loader.items()
])
print(snippets)
print([p.profile for p in snippets])
print(id(snippets[1].sources.raw))
print(id(snippets[2].sources.raw))
print(id(snippets[3].sources.raw))

Config.from_snippets("a", snippets)
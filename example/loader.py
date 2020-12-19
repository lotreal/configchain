from configchain.config import Config
from configchain.loader import ConfigLoader
from configchain.snippet import ConfigSnippet
from configchain.source import ConfigSource
from configchain.utils import list_flatten, inspect

loader = ConfigLoader("./test/asset/api.yaml")
loader.load()


def gs(conf: dict, file: str, index, dicts: list) -> ConfigSnippet:
    return ConfigSnippet(config=conf, source=ConfigSource(index=index, uri=file))


snippets = list_flatten(
    [
        [gs(d, file, index, dicts) for index, d in enumerate(dicts)]
        for file, dicts in loader.items()
    ]
)
dict()
# print(snippets)
# print([p.profile for p in snippets])
a = [
    Config.from_snippets(
        snippets=[
            ConfigSnippet(config=conf, source=ConfigSource(uri=uri, index=index))
            for index, conf in enumerate(dicts)
        ]
    )
    for uri, dicts in loader.items()
]

inspect(loader.items())
print()
inspect(a)

from configchain.config import Config
from configchain.loader import ConfigLoader
from configchain.snippet import ConfigSnippet
from configchain.source import ConfigSource, MergedConfigSource
from configchain.utils import list_flatten, inspect

loader = ConfigLoader("./test/asset/api.yaml")
loader.load()


snippets = list_flatten(loader.values())
inspect(snippets)

inspect(loader.items())


def find_in_loader(loader, file, key):
    snippets = loader.get(file)
    for s in snippets:
        v = s.config.get(key, None)
        if v is not None:
            return v
    return None


def find(source: ConfigSource, key):
    if isinstance(source, ConfigSource):
        return find_in_loader(loader, source.uri, key)
    if isinstance(source, MergedConfigSource):
        for uri in reversed([s.uri for s in source.sources]):
            v = find_in_loader(loader, uri, key)
            if v is not None:
                return v
    return "-"


def name(snippet: ConfigSnippet):
    def get(snippet, key):
        return snippet.config.get(key, find(snippet.source, key))

    group = get(snippet, "group")
    name = get(snippet, "name")
    print(group, name)


[name(s) for s in snippets]

#
# def gs(conf: dict, file: str, index, dicts: list) -> ConfigSnippet:
#     return ConfigSnippet(config=conf, source=ConfigSource(index=index, uri=file))
#
#
# snippets = list_flatten(
#     [
#         [gs(d, file, index, dicts) for index, d in enumerate(dicts)]
#         for file, dicts in loader.items()
#     ]
# )
# dict()
# # print(snippets)
# # print([p.profile for p in snippets])
# a = [
#     Config.from_snippets(
#         snippets=[
#             ConfigSnippet(config=conf, source=ConfigSource(uri=uri, index=index))
#             for index, conf in enumerate(dicts)
#         ]
#     )
#     for uri, dicts in loader.items()
# ]
#
# inspect(loader.items())
# print()
# inspect(a)

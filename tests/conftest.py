from configchain.snippet import ConfigSnippet
from configchain.source import ConfigSource


def cs(uri, index):
    return ConfigSource(uri=uri, index=index)


def snippet(conf: dict, uri="", index=0):
    return ConfigSnippet(config=conf, source=ConfigSource(uri=uri, index=index))


def snippets():
    s1 = ConfigSnippet(config={"a": 1}, source=cs("a", 1))
    s2 = ConfigSnippet(config={"a": 2}, source=cs("a", 2))
    s3 = ConfigSnippet(config={"a": 3}, source=cs("b", 3))
    s4 = ConfigSnippet(config={"a": 13, "profile": "tests"}, source=cs("b", 4))
    s5 = ConfigSnippet(config={"a": 14, "profile": "tests"}, source=cs("b", 5))
    return [s1, s2, s3, s4, s5]

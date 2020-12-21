from configchain.config import Config
from conftest import snippets, snippet


def test_con():
    c = Config.from_snippets(snippets=snippets())


def test_add():
    a = Config.from_snippets(
        snippets=[
            snippet({"a": 1}),
            snippet({"profile": "test", "a": 2}),
            snippet({"profile": "prod", "a": 3}),
        ]
    )
    b = Config.from_snippets(
        snippets=[
            snippet({"a": 1}),
            snippet({"profile": "test", "b": 2}),
            snippet({"profile": "stage", "b": 3}),
        ]
    )
    # print(a + b)

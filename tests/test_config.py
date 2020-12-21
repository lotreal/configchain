from configchain.config import Config
from conftest import snippets, snippet


def test_con():
    c = Config.from_snippets(snippets=snippets())


def test_add():
    a = Config.from_snippets(
        snippets=[
            snippet({"a": 1}),
            snippet({"profile": "tests", "a": 2}),
            snippet({"profile": "prod", "a": 3}),
        ]
    )
    assert list(a.keys()) == ["prod", "tests", "*"]
    b = Config.from_snippets(
        snippets=[
            snippet({"a": 1}),
            snippet({"profile": "tests", "b": 2}),
            snippet({"profile": "stage", "b": 3}),
        ]
    )
    assert list(b.keys()) == ["stage", "tests", "*"]
    c = a + b
    assert list(c.keys()) == ['prod', 'tests', '*', 'stage']
    assert c.get("tests").get("a") == 1


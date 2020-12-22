import pytest

from configchain.config import Config
from conftest import snippet


@pytest.fixture()
def a():
    return Config.from_snippets(
        snippets=[
            snippet({"g": 0}),
            snippet({"profile": "test", "t": 1, "tt": 1}),
            snippet({"profile": "uat", "u": 2}),
        ]
    )


@pytest.fixture()
def b():
    return Config.from_snippets(
        snippets=[snippet({"c": 1}), snippet({"profile": "test", "tt": 2, "ttt": 3}),]
    )


def test_config(a, b):
    assert list(a.keys()) == ["*", "test", "uat"]
    assert a.get("test").get("g") == 0
    assert list(b.keys()) == ["*", "test"]


def test_config2(a, b):
    b = Config.from_snippets(
        snippets=[snippet({"c": 1}), snippet({"tt": 2, "ttt": 3}),]
    )
    assert list(b.keys()) == ["*"]
    p = b.get("*")
    assert p.get("c") == 1
    assert p.get("tt") == 2
    assert p.get("ttt") == 3


def test_add(a, b):
    c = a + b
    assert list(c.keys()) == ["*", "test", "uat"]

    test = c.get("test")
    assert test.get("g") == 0
    assert test.get("c") == 1
    assert test.get("t") == 1
    assert test.get("tt") == 2
    assert test.get("ttt") == 3

    uat = c.get("uat")
    assert uat.get("g") == 0
    assert uat.get("c") == 1
    assert uat.get("u") == 2

    assert c.get("prod") is None
    prod = c.profile("prod")
    assert list(prod.keys()) == ["g", "c"]


def test_add2(a):
    b = Config.from_snippets(
        snippets=[snippet({"c": 1}), snippet({"profile": "prod", "tt": 2, "ttt": 3}),]
    )
    c = a + b
    assert list(c.keys()) == ["*", "prod", "test", "uat"]

    p = c.get("prod")
    assert p.get("g") == 0
    assert p.get("c") == 1
    assert p.get("t") is None
    assert p.get("tt") == 2
    assert p.get("ttt") == 3

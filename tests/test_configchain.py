from configchain import configchain
from configchain.utils import inspect


def test_a():
    cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", profile="profile")
    assert list(cs.keys()) == ["*"]
    print()
    inspect(cs)


def test_a_no_profile():
    cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", profile="foo")
    assert list(cs.keys()) == ["*"]
    print()
    inspect(cs)


def test_a_name():
    cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", name="app-${app}")
    assert list(cs.keys()) == ["app-hello", "*"]
    print()
    inspect(cs)

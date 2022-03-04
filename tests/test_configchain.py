import sys

from configchain import configchain
from configchain.utils import inspect


def test_a():
    # cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", group_by=ValueGrouper("${group}-${name}", "profile"))
    cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", profile="profile")
    assert list(cs.config_names()) == ["*"]
    assert list(cs.get_config("*").profile_names()) == ["*", "test"]
    # print()
    inspect(cs)
    # import yaml
    # yaml.dump(cs.get_config("*").get_profile("test"), sys.stdout)


def test_a_no_profile():
    cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", profile="foo")
    assert list(cs.config_names()) == ["*"]
    assert list(cs.get_config("*").profile_names()) == ["*"]
    print()
    inspect(cs)


def test_a_name():
    cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", name="app-${app}")
    assert list(cs.config_names()) == ["app-hello", "*"]
    print()
    inspect(cs)

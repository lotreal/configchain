from configchain.configset import ConfigSet, get_config_name
from conftest import snippet


def test_configset():
    configset = ConfigSet.load("./tests/asset/api.yaml")
    assert list(configset.keys()) == ["user-api", "user-gateway"]
    assert list(configset.get("user-api").keys()) == ["*", "stage", "testing"]
    assert list(configset.get("user-gateway").keys()) == ["*", "testing"]


def test_add():
    a = ConfigSet.load("./tests/asset/defaults.yaml")
    b = ConfigSet.load("./tests/asset/admin-api.yaml")
    c: ConfigSet = a + b
    assert c.get("user-api") is None


def test_get_config_name_by_statement():
    a = snippet({"g": 1, "b": 2, "a": 3})
    assert get_config_name(a, "[${a}/${g}]") == "[3/1]"


def test_get_config_name_by_fields():
    a = snippet({"g": 1, "b": 2, "a": 3})
    assert get_config_name(a, ["a", "g"]) == "3-1"


def test_get_config_name_by_statement_str():
    a = snippet({"g": 1, "b": 2, "a": 3})
    assert get_config_name(a, "aa") == "aa"


def test_get_config_name_by_statement_wildcard():
    a = snippet({"g": 1, "b": 2, "a": 3})
    assert get_config_name(a, "${aa}") == "*"


def test_get_config_name_by_fields_wildcard():
    a = snippet({"g": 1, "b": 2, "a": 3})
    assert get_config_name(a, ["aa", "gg"]) == "*"

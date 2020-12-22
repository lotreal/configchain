from configchain.configset import ConfigSet


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

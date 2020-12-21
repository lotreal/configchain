from configchain.configset import ConfigSet
from configchain.utils import inspect


def test_configset():
    configset = ConfigSet.load("./test/asset/api.yaml")
    assert list(configset.keys()) == ["user-api", "user-gateway"]
    assert list(configset.get("user-api").keys()) == ["stage", "testing", "*" ]
    assert list(configset.get("user-gateway").keys()) == ["testing", "*"]

def test_add():
    a = ConfigSet.load("./test/asset/default.yaml")
    b = ConfigSet.load("./test/asset/api.yaml")
    c: ConfigSet = a + b
    assert c.get("user-api").get("testing").get("test")
    inspect(c)

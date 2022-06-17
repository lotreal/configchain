from configchain import configchain


def test_configset():
    configset = configchain("./tests/asset/multi.yaml", name="${group}-${name}")
    assert list(configset.keys()) == ["*", "user-gateway", "user-web"]
    assert list(configset.get("user-web").keys()) == ["*", "testing"]
    assert list(configset.get("user-gateway").keys()) == ["*", "testing"]
    print(configset)
    assert configset.get("user-web").get("testing").get("from") == "web"
    assert configset.get("user-web").get("testing").get("web") == "test"
    assert configset.get("user-web").get("*").get("from") == "web"
    assert configset.get("user-web").get("*").get("web") is None
    assert configset.get("user-web").get("testing").get("docker") == "service2"
    assert configset.get("user-gateway").get("testing").get("docker") == "service"
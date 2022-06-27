from configchain import configchain


class GithubLoader:
    repository: str

    def __init__(self, repository, path=""):
        pass


def test_configset():
    """
    configchain(
        "default.yaml",
        "https://github.com/infinitas-plus/user-service/blob/main/.cmdb.yaml",
        GithubLoader(repository="infinitas-plus/user-service", path="/.cmdb.yaml"),
    )
    configset = configchain(
        "./tests/asset/defaults.yaml",
        "./tests/asset/multi.yaml",
        GithubLoader(repository="infinitas-plus/user-service", path="/.cmdb.yaml"),
        name="${group}-${name}",
        loader=GithubLoader(repository="infinitas-plus/search-service"),
    )
    """
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

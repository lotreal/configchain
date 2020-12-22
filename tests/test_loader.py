from configchain.loader import ConfigLoader


def test_load():
    loader = ConfigLoader("./tests/asset/api.yaml")
    loader.load()

    assert len(loader.keys()) == 3
    assert len(loader.values()) == 3

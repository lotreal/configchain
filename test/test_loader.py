from configchain.loader import ConfigLoader


def test_load():
    loader = ConfigLoader("./test/asset/api.yaml")
    loader.load()

    assert len(loader.keys()) == 3
    assert len(loader.values()) == 3
    # print(loader.popitem()[1])
    # assert loader.popitem()[1][1]["environment"][0] == "PROCESSES=4"
    # assert loader.popitem()[1][1]["environment"][0] == "PROCESSES=2"

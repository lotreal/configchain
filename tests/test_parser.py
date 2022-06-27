from configchain.loader import FileLoader
from configchain.parser import ConfigParser
from configchain.source import ConfigSource


class MockLoader:
    def __init__(self, workdir: str = None):
        self.workdir = workdir

    def key(self, file):
        return file

    def read(self, relative_path):
        ConfigSource(
            index=1,
            # name="api",
            uri="api.yaml",
            # is_entrypoint=True,
        )
        return f"content: {relative_path}"


def test_load1():
    loader = ConfigParser("./tests/asset/api.yaml", reader=FileLoader())
    loader.load()

    assert list(loader.keys()) == [
        "/Users/luotao/Entropy/lotreal/configchain/tests/asset/api.yaml",
        "/Users/luotao/Entropy/lotreal/configchain/tests/asset/gateway.yaml",
        "/Users/luotao/Entropy/lotreal/configchain/tests/asset/api-stage.yaml",
    ]
    assert str(loader.get("/Users/luotao/Entropy/lotreal/configchain/tests/asset/gateway.yaml")[0].source) == "api-2-gateway-0"
    assert len(loader.keys()) == 3
    assert len(loader.values()) == 3


def test_load2():
    loader = ConfigParser("./tests/asset/api.yaml", reader=MockLoader())
    loader.load()

    assert len(loader.keys()) == 1
    assert len(loader.values()) == 1

from configchain.snippet import ConfigSnippet, ChainedConfigSnippet
from conftest import cs


def test_chained():
    s1 = ConfigSnippet(config={"a": 1}, source=cs("a", 1))
    s2 = ConfigSnippet(config={"a": 2}, source=cs("a", 2))
    s3 = ConfigSnippet(config={"a": 3}, source=cs("b", 3))

    s4 = ChainedConfigSnippet(nodes=[s1, s2, s3]).build()
    assert s4.get("a") == 3
    assert str(s4.source) == "a-1-2-b-3"



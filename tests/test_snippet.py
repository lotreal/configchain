from conftest import snippets


def test_add():
    s1, s2, s3, *_ = snippets()
    s4 = s1 + s2 + s3
    assert s4.get("a") == 3
    assert str(s4.source) == "a-1-2-b-3"
    assert s4.profile == "*"

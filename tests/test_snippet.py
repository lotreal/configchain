from copy import deepcopy, copy

from conftest import snippets, snippet


def test_copy():
    a = snippet({"a": 1})
    b = copy(a)
    assert a == b
    assert id(a) != id(b)
    assert id(a.source) == id(b.source)
    assert a == deepcopy(b)


def test_eq():
    assert snippet({"a": 1}) == snippet({"a": 1})
    assert snippet({"a": 1}) != snippet({"a": 2})


def test_add():
    s1, s2, s3, *_ = snippets()
    s4 = s1 + s2 + s3
    assert s4.get("a") == 3
    assert str(s4.source) == "a-1-2-b-3"

from conftest import cs


def ensure_add_implements(a, b):
    ida = id(a)
    idb = id(b)
    c = a + b
    idc = id(c)
    assert ida != idc
    assert idb != idc
    return c


def test_add():
    a = cs("a", 0)
    b = cs("b", 1)
    c = ensure_add_implements(a, b)
    assert str(c) == "a-0-b-1"

    d = cs("d", 3)
    e = ensure_add_implements(c, d)
    assert str(e) == "a-0-b-1-d-3"

    assert id(c) != id(e)


def test_add2():
    assert str(cs("a", 1) + cs("a", 2)) == "a-1-2"
    assert str(cs("a", 1) + cs("a", 2) + cs("b", 1)) == "a-1-2-b-1"


def test_eq():
    assert cs("a", 1) == cs("a", 1)
    assert cs("a", 1) + cs("b", 2) == cs("a", 1) + cs("b", 2)


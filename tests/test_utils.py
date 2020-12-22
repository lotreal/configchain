from collections import OrderedDict
from operator import add

from configchain.utils import dict_merge


def test_dict_merge():
    a = OrderedDict({"a": 1, "b": 2})
    b = OrderedDict({"b": 2, "c": 3})
    c = dict_merge(a, b, add)
    assert list(a.keys()) == ["a", "b"]
    assert list(b.keys()) == ["b", "c"]
    assert list(c.keys()) == ["a", "b", "c"]
    assert c.get("b") == 4

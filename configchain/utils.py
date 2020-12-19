from functools import singledispatch
from itertools import groupby
from typing import Callable, TypeVar, Dict, List, Any
import pprint

KT = TypeVar("KT")
VT = TypeVar("VT")


pp = pprint.PrettyPrinter()


def inspect(obj):
    pp.pprint(obj)


def list_flatten(t: list):
    return [item for sublist in t for item in sublist]


def list_groupby(iterable: List[Any], projection) -> List[List[Any]]:
    return [list(it) for k, it in groupby(sorted(iterable, key=projection), projection)]


def dict_merge(
    a: Dict[KT, VT], b: Dict[KT, VT], f: Callable[[VT, VT], VT]
) -> Dict[KT, VT]:
    merged = {k: a.get(k, b.get(k)) for k in a.keys() ^ b.keys()}
    merged.update({k: f(a[k], b[k]) for k in a.keys() & b.keys()})
    return merged


@singledispatch
def config_merger(_, b):
    return b


@config_merger.register
def _(a: dict, b: dict):
    return dict_merge(a, b, config_merger)


@config_merger.register
def _(a: list, b: list):
    return a + b

from copy import copy
from functools import singledispatch
from itertools import groupby
from typing import Callable, Dict, List, Any
import pprint
from .types import KT, VT, PROFILE_GLOBAL


def inspect(obj):
    pp = pprint.PrettyPrinter()
    pp.pprint(obj)


def list_flatten(t: List[List[Any]]) -> List[Any]:
    return [item for sublist in t for item in sublist]


def list_groupby(iterable: List[Any], projection) -> List[List[Any]]:
    return [list(it) for k, it in groupby(sorted(iterable, key=projection), projection)]


def list_uniq(a: List[Any]) -> List[Any]:
    return list(dict.fromkeys(a))


def dict_merge(
    a: Dict[KT, VT], b: Dict[KT, VT], f: Callable[[VT, VT], VT]
) -> Dict[KT, VT]:
    if b is None:
        return a

    merged = copy(a)
    for k in b.keys():
        if k in merged.keys():
            merged[k] = f(a[k], b[k])
        else:
            merged[k] = b[k]
    return merged


def dict_merge_with_wildcard(
    a: Dict[KT, VT], b: Dict[KT, VT], f: Callable[[VT, VT], VT]
) -> Dict[KT, VT]:
    if b is None:
        return a

    merged = copy(b)
    wb = b.get(PROFILE_GLOBAL, None)
    for k in a.keys():
        if k in b.keys():
            merged[k] = f(a[k], b[k])
        else:
            merged[k] = f(a[k], wb)

    wa = a.get(PROFILE_GLOBAL, None)
    if wa is not None:
        for k in b.keys():
            if k not in a.keys():
                merged[k] = f(wa, b[k])
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

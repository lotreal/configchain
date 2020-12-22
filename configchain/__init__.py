from functools import reduce
from operator import add

from .configset import ConfigSet


def configchain(*files, **kwargs):
    return reduce(add, [ConfigSet.load(f) for f in files])

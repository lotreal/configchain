from functools import reduce
from operator import add
from typing import Any

from .snippet import ConfigSnippet
from .config import Config
from .configset import ConfigSet
from .types import ConfigFile


def configchain(*files: ConfigFile, **kwargs: Any):
    return reduce(add, [ConfigSet.load(f, **kwargs) for f in files])

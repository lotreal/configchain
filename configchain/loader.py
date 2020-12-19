from abc import ABC, abstractmethod
from collections import OrderedDict
from os import path

import yaml


class BaseConfigLoader(OrderedDict, ABC):
    @abstractmethod
    def load(self):
        ...


class YamlConfigLoader(BaseConfigLoader):
    """
    Key: the path of loaded yaml
    Value: the config dict of yaml
    """

    def __init__(self, *files: str):
        self._source = files
        self._includes = []

    def load(self):
        [self._load(file) for file in self._source]

    def _load(self, file: str) -> None:
        key = path.abspath(file)
        if key in self.keys():
            return
        with open(file, "r") as fh:
            _content = fh.read()
        _conf = yaml.load_all(_content, Loader=yaml.SafeLoader)
        d = [self._process_directives(file, c) for c in _conf]
        self.setdefault(path.abspath(file), [dc for dc in d if dc])

        while self._includes:
            self._load(self._includes.pop())

    def _process_directives(self, file, config: dict) -> dict:
        workdir = path.dirname(file)
        includes = config.pop("@include", None)
        if includes is not None:
            self._includes.extend(
                [path.abspath(path.join(workdir, f)) for f in includes]
            )

        return config


class ConfigLoader(object):
    def __new__(cls, *args, **kwargs):
        return YamlConfigLoader(*args, **kwargs)

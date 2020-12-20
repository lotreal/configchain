from abc import ABC, abstractmethod
from collections import OrderedDict
from os import path

import yaml

from configchain.snippet import ConfigSnippet
from configchain.source import ConfigSource


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

    def _read_file(self, file):
        key = path.abspath(file)
        if key in self.keys():
            return None
        with open(file, "r") as fh:
            return fh.read()

    def _parse_config(self, content):
        if content is None:
            return []
        return yaml.load_all(content, Loader=yaml.SafeLoader)

    def _load(self, file: str, source = None) -> None:
        file = path.abspath(file)
        _conf = self._parse_config(self._read_file(file))

        configs = [self._process_directives(file, c) for c in _conf]
        configs = [dc for dc in configs if dc]


        def gs(config, file, index, ps=None):
            source = ConfigSource(uri=file, index=index)
            if ps is not None:
                source = ps + source
            return ConfigSnippet(config=config, source=source)

        snippets = [gs(config, file, index, source) for index, config in enumerate(configs)]
        self.setdefault(file, snippets)

        while self._includes:
            inc, source = self._includes.pop()
            self._load(inc, source)

    def _process_directives(self, file, config: dict) -> dict:
        workdir = path.dirname(file)
        includes = config.pop("@include", None)
        if includes is not None:
            self._includes.extend(
                [(path.abspath(path.join(workdir, f)),
                  ConfigSource(uri=file, index=0)
                  ) for f in includes]
            )

        return config


class ConfigLoader(object):
    def __new__(cls, *args, **kwargs):
        return YamlConfigLoader(*args, **kwargs)

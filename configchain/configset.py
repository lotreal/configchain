from typing import List

from .config import Config
from .loader import ConfigLoader
from .snippet import ConfigSnippet
from .utils import list_flatten, inspect


class ConfigSet(object):
    @classmethod
    def load(cls, *args, **kwargs):
        loader = ConfigLoader(*args, **kwargs)
        loader.load()

        snippets = list_flatten(loader.values())
        inspect(snippets)

        def name(snippet: ConfigSnippet, from_fields: List[str]):
            ids = [
                n
                for n in [snippet.find(field) for field in from_fields]
                if n is not None
            ]
            if ids:
                return "-".join(ids)
            else:
                return "*"

        named_snippets = dict()
        for snippet in snippets:
            named_snippets.setdefault(name(snippet, ["group", "name"]), []).append(
                snippet
            )

        named_configs = {
            name: Config.from_snippets(snippets)
            for name, snippets in named_snippets.items()
        }
        return named_configs

    def __add__(self, other):
        pass
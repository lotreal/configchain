from typing import TypeVar, List, Union, Mapping, Callable

ConfigFile = str
ConfigName = str

ConfigKey = str
ConfigValue = Union[List[Union[str, int]], "ConfigDict", str, int]
ConfigDict = Mapping[ConfigKey, ConfigValue]

ProfileKey = str
ProfileName = str

WILDCARD = "*"
PROFILE_NAME_KEY = "profile"
CONFIG_NAME_KEY = ["group", "name"]
ConfigNameGetter = Callable[["ConfigSnippet"], ConfigName]

KT = TypeVar("KT")
VT = TypeVar("VT")

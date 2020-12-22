from typing import TypeVar, List, Union, Mapping

ConfigFile = str
ConfigName = str

ConfigKey = str
ConfigValue = Union[List[Union[str, int]], "ConfigDict", str, int]
ConfigDict = Mapping[ConfigKey, ConfigValue]

ProfileKey = str
ProfileName = str

PROFILE_GLOBAL = "*"

KT = TypeVar("KT")
VT = TypeVar("VT")

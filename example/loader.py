from configchain.configset import ConfigSet
from configchain.utils import inspect

configset = ConfigSet.load("./test/asset/api.yaml")
inspect(configset)

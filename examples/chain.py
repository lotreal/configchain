from configchain import configchain
from configchain.utils import inspect

cs = configchain("./tests/asset/a.yaml", "./tests/asset/b.yaml", name="app-${app}", profile="profile")
inspect(cs)
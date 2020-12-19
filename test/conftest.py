from configchain.source import ConfigSource


def cs(uri, index):
    return ConfigSource(uri=uri, index=index)

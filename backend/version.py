from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except:
    __version__ = ""

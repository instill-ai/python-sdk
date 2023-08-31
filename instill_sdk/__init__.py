from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("instill-python-sdk")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version

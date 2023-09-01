import sys
from importlib.metadata import PackageNotFoundError, version

from instill_sdk.utils.logger import Logger

Logger.initialize()
sys.path.insert(0, "./instill_sdk/protogen")

try:
    __version__ = version("instill-python-sdk")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version

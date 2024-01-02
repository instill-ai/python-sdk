# pylint: disable=no-name-in-module
import os
import sys
from importlib.metadata import PackageNotFoundError, version

from instill.utils.logger import Logger

Logger.initialize()

sys.path.append(os.path.join(os.path.dirname(__file__), "protogen"))

try:
    __version__ = version("instill-sdk")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version

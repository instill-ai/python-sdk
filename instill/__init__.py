# pylint: disable=no-name-in-module,wrong-import-position
import os
import sys
from importlib.metadata import PackageNotFoundError, version

from instill.utils.logger import Logger

Logger.initialize()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "protogen"))

# protogen `model` package collides with `model.py`
# temporarily remove current directory from sys.path
# and import ray_io
if "" in sys.path:
    sys.path.remove("")
    import instill.helpers.ray_io

    sys.path.insert(0, "")

try:
    __version__ = version("instill-sdk")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version

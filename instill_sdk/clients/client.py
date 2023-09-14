# pylint: disable=no-member,wrong-import-position
import os
from abc import ABC, abstractmethod

API_TOKEN = os.environ.get("INSTILL_AI_API_TOKEN", default="")


class Client(ABC):
    """Base interface class for creating mgmt/pipeline/connector/model clients.

    Args:
        ABC (abc.ABCMeta): std abstract class
    """

    @property
    @abstractmethod
    def token(self):
        pass

    @token.setter
    @abstractmethod
    def token(self):
        pass

    @property
    @abstractmethod
    def host(self):
        pass

    @host.setter
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def port(self):
        pass

    @port.setter
    @abstractmethod
    def port(self):
        pass

    @abstractmethod
    def liveness(self):
        raise NotImplementedError

    @abstractmethod
    def readiness(self):
        raise NotImplementedError

    @abstractmethod
    def is_serving(self):
        raise NotImplementedError

# pylint: disable=no-member,wrong-import-position
from abc import ABC, abstractmethod


class Resource(ABC):
    """Base interface class for creating resources.

    Args:
        ABC (abc.ABCMeta): std abstract class
    """

    @property
    @abstractmethod
    def client(self):
        pass

    @client.setter
    @abstractmethod
    def client(self):
        pass

    @property
    @abstractmethod
    def resource(self):
        pass

    @resource.setter
    @abstractmethod
    def resource(self):
        pass

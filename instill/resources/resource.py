"""Base resource interface module."""

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
        """Get the client instance."""

    @client.setter
    @abstractmethod
    def client(self, value):
        """Set the client instance."""

    @property
    @abstractmethod
    def resource(self):
        """Get the resource instance."""

    @resource.setter
    @abstractmethod
    def resource(self, value):
        """Set the resource instance."""

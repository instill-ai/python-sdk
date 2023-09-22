from abc import ABC, abstractmethod


class Client(ABC):
    """Base interface class for creating mgmt/pipeline/connector/model clients.

    Args:
        ABC (abc.ABCMeta): std abstract class
    """

    @property
    @abstractmethod
    def hosts(self):
        pass

    @hosts.setter
    @abstractmethod
    def hosts(self):
        pass

    @property
    @abstractmethod
    def instance(self):
        pass

    @instance.setter
    @abstractmethod
    def instance(self):
        pass

    @property
    @abstractmethod
    def metadata(self):
        pass

    @metadata.setter
    @abstractmethod
    def metadata(self):
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

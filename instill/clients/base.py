from abc import ABC, abstractmethod
from typing import Union

import google.protobuf.message
import grpc


class Client(ABC):
    """Base interface class for creating mgmt/pipeline/model clients.

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


class RequestFactory:
    def __init__(
        self,
        method: Union[grpc.UnaryUnaryMultiCallable, grpc.StreamUnaryMultiCallable],
        request: google.protobuf.message.Message,
        metadata,
    ) -> None:
        self.method = method
        self.request = request
        self.metadata = metadata

    def send_sync(self):
        return self.method(request=self.request, metadata=self.metadata)

    def send_stream(self):
        return self.method(
            request_iterator=iter([self.request]),
            metadata=self.metadata,
        )

    async def send_async(self):
        return await self.method(request=self.request, metadata=self.metadata)

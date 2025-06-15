"""Base client interface module."""

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
    def host(self):
        """Get the host address."""

    @host.setter
    @abstractmethod
    def host(self, value):
        """Set the host address."""

    @property
    @abstractmethod
    def metadata(self):
        """Get the metadata."""

    @metadata.setter
    @abstractmethod
    def metadata(self, value):
        """Set the metadata."""

    @abstractmethod
    def liveness(self):
        """Check if the service is alive."""
        raise NotImplementedError

    @abstractmethod
    def readiness(self):
        """Check if the service is ready to serve."""
        raise NotImplementedError

    @abstractmethod
    def is_serving(self):
        """Check if the service is currently serving."""
        raise NotImplementedError


class RequestFactory:
    """Factory class for creating and sending gRPC requests."""

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
        """Send a synchronous gRPC request."""
        return self.method(request=self.request, metadata=self.metadata)

    def send_stream(self):
        """Send a streaming gRPC request."""
        return self.method(
            request_iterator=iter([self.request]),
            metadata=self.metadata,
        )

    async def send_async(self):
        """Send an asynchronous gRPC request."""
        return await self.method(request=self.request, metadata=self.metadata)

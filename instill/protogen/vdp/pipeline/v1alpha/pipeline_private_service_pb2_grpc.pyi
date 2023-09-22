"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import collections.abc
import grpc
import grpc.aio
import typing
import vdp.pipeline.v1alpha.operator_definition_pb2
import vdp.pipeline.v1alpha.pipeline_pb2

_T = typing.TypeVar('_T')

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta):
    ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore
    ...

class PipelinePrivateServiceStub:
    """Pipeline service responds to internal access"""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    ListPipelinesAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminResponse,
    ]
    """ListPipelinesAdmin method receives a ListPipelinesAdminRequest message and
    returns a ListPipelinesAdminResponse message.
    """
    LookUpPipelineAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminResponse,
    ]
    """LookUpPipelineAdmin method receives a LookUpPipelineAdminRequest message
    and returns a LookUpPipelineAdminResponse
    """
    LookUpOperatorDefinitionAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminRequest,
        vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse,
    ]
    """LookUpOperatorDefinitionAdmin method receives a
    LookUpOperatorDefinitionAdminRequest message and returns a
    LookUpOperatorDefinitionAdminResponse
    """
    ListPipelineReleasesAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminResponse,
    ]
    """ListPipelineReleasesAdmin method receives a ListPipelineReleasesAdminRequest message and
    returns a ListPipelineReleasesAdminResponse message.
    """

class PipelinePrivateServiceAsyncStub:
    """Pipeline service responds to internal access"""

    ListPipelinesAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminResponse,
    ]
    """ListPipelinesAdmin method receives a ListPipelinesAdminRequest message and
    returns a ListPipelinesAdminResponse message.
    """
    LookUpPipelineAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminResponse,
    ]
    """LookUpPipelineAdmin method receives a LookUpPipelineAdminRequest message
    and returns a LookUpPipelineAdminResponse
    """
    LookUpOperatorDefinitionAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminRequest,
        vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse,
    ]
    """LookUpOperatorDefinitionAdmin method receives a
    LookUpOperatorDefinitionAdminRequest message and returns a
    LookUpOperatorDefinitionAdminResponse
    """
    ListPipelineReleasesAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminResponse,
    ]
    """ListPipelineReleasesAdmin method receives a ListPipelineReleasesAdminRequest message and
    returns a ListPipelineReleasesAdminResponse message.
    """

class PipelinePrivateServiceServicer(metaclass=abc.ABCMeta):
    """Pipeline service responds to internal access"""

    @abc.abstractmethod
    def ListPipelinesAdmin(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesAdminResponse]]:
        """ListPipelinesAdmin method receives a ListPipelinesAdminRequest message and
        returns a ListPipelinesAdminResponse message.
        """
    @abc.abstractmethod
    def LookUpPipelineAdmin(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineAdminResponse]]:
        """LookUpPipelineAdmin method receives a LookUpPipelineAdminRequest message
        and returns a LookUpPipelineAdminResponse
        """
    @abc.abstractmethod
    def LookUpOperatorDefinitionAdmin(
        self,
        request: vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse]]:
        """LookUpOperatorDefinitionAdmin method receives a
        LookUpOperatorDefinitionAdminRequest message and returns a
        LookUpOperatorDefinitionAdminResponse
        """
    @abc.abstractmethod
    def ListPipelineReleasesAdmin(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ListPipelineReleasesAdminResponse]]:
        """ListPipelineReleasesAdmin method receives a ListPipelineReleasesAdminRequest message and
        returns a ListPipelineReleasesAdminResponse message.
        """

def add_PipelinePrivateServiceServicer_to_server(servicer: PipelinePrivateServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...

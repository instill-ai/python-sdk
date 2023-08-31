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

class PipelinePublicServiceStub:
    """Pipeline service responds to external access"""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Liveness: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.LivenessRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.LivenessResponse,
    ]
    """Liveness method receives a LivenessRequest message and returns a
    LivenessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    Readiness: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ReadinessRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ReadinessResponse,
    ]
    """Readiness method receives a ReadinessRequest message and returns a
    ReadinessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    ListOperatorDefinitions: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsRequest,
        vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsResponse,
    ]
    """ListOperatorDefinitions method receives a
    ListOperatorDefinitionsRequest message and returns a
    ListOperatorDefinitionsResponse message.
    """
    GetOperatorDefinition: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionRequest,
        vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionResponse,
    ]
    """GetOperatorDefinition method receives a
    GetOperatorDefinitionRequest message and returns a
    GetGetOperatorDefinitionResponse message.
    """
    ListPipelines: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesResponse,
    ]
    """ListPipelines method receives a ListPipelinesRequest message and returns a
    ListPipelinesResponse message.
    """
    LookUpPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineResponse,
    ]
    """LookUpPipeline method receives a LookUpPipelineRequest message and returns
    a LookUpPipelineResponse
    """
    CreateUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineResponse,
    ]
    """CreateUserPipeline method receives a CreateUserPipelineRequest message and returns
    a CreateUserPipelineResponse message.
    """
    ListUserPipelines: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesResponse,
    ]
    """ListUserPipelines method receives a ListUserPipelinesRequest message and returns a
    ListUserPipelinesResponse message.
    """
    GetUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineResponse,
    ]
    """GetUserPipeline method receives a GetUserPipelineRequest message and returns a
    GetUserPipelineResponse message.
    """
    UpdateUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineResponse,
    ]
    """UpdateUserPipeline method receives a UpdateUserPipelineRequest message and returns
    a UpdateUserPipelineResponse message.
    """
    DeleteUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineResponse,
    ]
    """DeleteUserPipeline method receives a DeleteUserPipelineRequest message and returns
    a DeleteUserPipelineResponse message.
    """
    ValidateUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineResponse,
    ]
    """Validate a pipeline."""
    RenameUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineResponse,
    ]
    """RenameUserPipeline method receives a RenameUserPipelineRequest message and returns
    a RenameUserPipelineResponse message.
    """
    TriggerUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineResponse,
    ]
    """TriggerUserPipeline method receives a TriggerUserPipelineRequest message
    and returns a TriggerUserPipelineResponse.
    """
    TriggerAsyncUserPipeline: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineResponse,
    ]
    """TriggerAsyncUserPipeline method receives a TriggerAsyncUserPipelineRequest message and
    returns a TriggerAsyncUserPipelineResponse.
    """
    GetOperation: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.GetOperationRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.GetOperationResponse,
    ]
    """*Longrunning operation methods

    GetOperation method receives a
    GetOperationRequest message and returns a
    GetOperationResponse message.
    """
    CreateUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseResponse,
    ]
    """CreateUserPipelineRelease method receives a CreateUserPipelineReleaseRequest message and returns
    a CreateUserPipelineReleaseResponse message.
    """
    ListUserPipelineReleases: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesResponse,
    ]
    """ListUserPipelineReleases method receives a ListUserPipelineReleasesRequest message and returns a
    ListUserPipelineReleasesResponse message.
    """
    GetUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseResponse,
    ]
    """GetUserPipelineRelease method receives a GetUserPipelineReleaseRequest message and returns a
    GetUserPipelineReleaseResponse message.
    """
    UpdateUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseResponse,
    ]
    """UpdateUserPipelineRelease method receives a UpdateUserPipelineReleaseRequest message and returns
    a UpdateUserPipelineReleaseResponse message.
    """
    DeleteUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseResponse,
    ]
    """DeleteUserPipelineRelease method receives a DeleteUserPipelineReleaseRequest message and returns
    a DeleteUserPipelineReleaseResponse message.
    """
    RestoreUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseResponse,
    ]
    """RestoreUserPipelineRelease method receives a RestoreUserPipelineReleaseRequest message
    and returns a RestoreUserPipelineReleaseResponse
    """
    SetDefaultUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseResponse,
    ]
    """SetDefaultUserPipelineRelease method receives a SetDefaultUserPipelineReleaseRequest message
    and returns a SetDefaultUserPipelineReleaseResponse
    """
    WatchUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseResponse,
    ]
    """WatchUserPipelineRelease method receives a WatchUserPipelineReleaseRequest message
    and returns a WatchUserPipelineReleaseResponse
    """
    RenameUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseResponse,
    ]
    """RenameUserPipelineRelease method receives a RenameUserPipelineReleaseRequest message and returns
    a RenameUserPipelineReleaseResponse message.
    """
    TriggerUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseResponse,
    ]
    """TriggerUserPipelineRelease method receives a TriggeUserPipelineReleaseRequest message
    and returns a TriggerPipelineReleasePipelineResponse.
    """
    TriggerAsyncUserPipelineRelease: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseResponse,
    ]
    """TriggerAsyncUserPipelineRelease method receives a TriggerAsyncUserPipelineReleaseRequest message and
    returns a TriggerAsyncUserPipelineReleaseResponse.
    """

class PipelinePublicServiceAsyncStub:
    """Pipeline service responds to external access"""

    Liveness: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.LivenessRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.LivenessResponse,
    ]
    """Liveness method receives a LivenessRequest message and returns a
    LivenessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    Readiness: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ReadinessRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ReadinessResponse,
    ]
    """Readiness method receives a ReadinessRequest message and returns a
    ReadinessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    ListOperatorDefinitions: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsRequest,
        vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsResponse,
    ]
    """ListOperatorDefinitions method receives a
    ListOperatorDefinitionsRequest message and returns a
    ListOperatorDefinitionsResponse message.
    """
    GetOperatorDefinition: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionRequest,
        vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionResponse,
    ]
    """GetOperatorDefinition method receives a
    GetOperatorDefinitionRequest message and returns a
    GetGetOperatorDefinitionResponse message.
    """
    ListPipelines: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesResponse,
    ]
    """ListPipelines method receives a ListPipelinesRequest message and returns a
    ListPipelinesResponse message.
    """
    LookUpPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineResponse,
    ]
    """LookUpPipeline method receives a LookUpPipelineRequest message and returns
    a LookUpPipelineResponse
    """
    CreateUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineResponse,
    ]
    """CreateUserPipeline method receives a CreateUserPipelineRequest message and returns
    a CreateUserPipelineResponse message.
    """
    ListUserPipelines: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesResponse,
    ]
    """ListUserPipelines method receives a ListUserPipelinesRequest message and returns a
    ListUserPipelinesResponse message.
    """
    GetUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineResponse,
    ]
    """GetUserPipeline method receives a GetUserPipelineRequest message and returns a
    GetUserPipelineResponse message.
    """
    UpdateUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineResponse,
    ]
    """UpdateUserPipeline method receives a UpdateUserPipelineRequest message and returns
    a UpdateUserPipelineResponse message.
    """
    DeleteUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineResponse,
    ]
    """DeleteUserPipeline method receives a DeleteUserPipelineRequest message and returns
    a DeleteUserPipelineResponse message.
    """
    ValidateUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineResponse,
    ]
    """Validate a pipeline."""
    RenameUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineResponse,
    ]
    """RenameUserPipeline method receives a RenameUserPipelineRequest message and returns
    a RenameUserPipelineResponse message.
    """
    TriggerUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineResponse,
    ]
    """TriggerUserPipeline method receives a TriggerUserPipelineRequest message
    and returns a TriggerUserPipelineResponse.
    """
    TriggerAsyncUserPipeline: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineResponse,
    ]
    """TriggerAsyncUserPipeline method receives a TriggerAsyncUserPipelineRequest message and
    returns a TriggerAsyncUserPipelineResponse.
    """
    GetOperation: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.GetOperationRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.GetOperationResponse,
    ]
    """*Longrunning operation methods

    GetOperation method receives a
    GetOperationRequest message and returns a
    GetOperationResponse message.
    """
    CreateUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseResponse,
    ]
    """CreateUserPipelineRelease method receives a CreateUserPipelineReleaseRequest message and returns
    a CreateUserPipelineReleaseResponse message.
    """
    ListUserPipelineReleases: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesResponse,
    ]
    """ListUserPipelineReleases method receives a ListUserPipelineReleasesRequest message and returns a
    ListUserPipelineReleasesResponse message.
    """
    GetUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseResponse,
    ]
    """GetUserPipelineRelease method receives a GetUserPipelineReleaseRequest message and returns a
    GetUserPipelineReleaseResponse message.
    """
    UpdateUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseResponse,
    ]
    """UpdateUserPipelineRelease method receives a UpdateUserPipelineReleaseRequest message and returns
    a UpdateUserPipelineReleaseResponse message.
    """
    DeleteUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseResponse,
    ]
    """DeleteUserPipelineRelease method receives a DeleteUserPipelineReleaseRequest message and returns
    a DeleteUserPipelineReleaseResponse message.
    """
    RestoreUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseResponse,
    ]
    """RestoreUserPipelineRelease method receives a RestoreUserPipelineReleaseRequest message
    and returns a RestoreUserPipelineReleaseResponse
    """
    SetDefaultUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseResponse,
    ]
    """SetDefaultUserPipelineRelease method receives a SetDefaultUserPipelineReleaseRequest message
    and returns a SetDefaultUserPipelineReleaseResponse
    """
    WatchUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseResponse,
    ]
    """WatchUserPipelineRelease method receives a WatchUserPipelineReleaseRequest message
    and returns a WatchUserPipelineReleaseResponse
    """
    RenameUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseResponse,
    ]
    """RenameUserPipelineRelease method receives a RenameUserPipelineReleaseRequest message and returns
    a RenameUserPipelineReleaseResponse message.
    """
    TriggerUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseResponse,
    ]
    """TriggerUserPipelineRelease method receives a TriggeUserPipelineReleaseRequest message
    and returns a TriggerPipelineReleasePipelineResponse.
    """
    TriggerAsyncUserPipelineRelease: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseRequest,
        vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseResponse,
    ]
    """TriggerAsyncUserPipelineRelease method receives a TriggerAsyncUserPipelineReleaseRequest message and
    returns a TriggerAsyncUserPipelineReleaseResponse.
    """

class PipelinePublicServiceServicer(metaclass=abc.ABCMeta):
    """Pipeline service responds to external access"""

    @abc.abstractmethod
    def Liveness(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.LivenessRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.LivenessResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.LivenessResponse]]:
        """Liveness method receives a LivenessRequest message and returns a
        LivenessResponse message.
        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
    @abc.abstractmethod
    def Readiness(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ReadinessRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ReadinessResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ReadinessResponse]]:
        """Readiness method receives a ReadinessRequest message and returns a
        ReadinessResponse message.
        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
    @abc.abstractmethod
    def ListOperatorDefinitions(
        self,
        request: vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.operator_definition_pb2.ListOperatorDefinitionsResponse]]:
        """ListOperatorDefinitions method receives a
        ListOperatorDefinitionsRequest message and returns a
        ListOperatorDefinitionsResponse message.
        """
    @abc.abstractmethod
    def GetOperatorDefinition(
        self,
        request: vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.operator_definition_pb2.GetOperatorDefinitionResponse]]:
        """GetOperatorDefinition method receives a
        GetOperatorDefinitionRequest message and returns a
        GetGetOperatorDefinitionResponse message.
        """
    @abc.abstractmethod
    def ListPipelines(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ListPipelinesResponse]]:
        """ListPipelines method receives a ListPipelinesRequest message and returns a
        ListPipelinesResponse message.
        """
    @abc.abstractmethod
    def LookUpPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.LookUpPipelineResponse]]:
        """LookUpPipeline method receives a LookUpPipelineRequest message and returns
        a LookUpPipelineResponse
        """
    @abc.abstractmethod
    def CreateUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineResponse]]:
        """CreateUserPipeline method receives a CreateUserPipelineRequest message and returns
        a CreateUserPipelineResponse message.
        """
    @abc.abstractmethod
    def ListUserPipelines(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelinesResponse]]:
        """ListUserPipelines method receives a ListUserPipelinesRequest message and returns a
        ListUserPipelinesResponse message.
        """
    @abc.abstractmethod
    def GetUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineResponse]]:
        """GetUserPipeline method receives a GetUserPipelineRequest message and returns a
        GetUserPipelineResponse message.
        """
    @abc.abstractmethod
    def UpdateUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineResponse]]:
        """UpdateUserPipeline method receives a UpdateUserPipelineRequest message and returns
        a UpdateUserPipelineResponse message.
        """
    @abc.abstractmethod
    def DeleteUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineResponse]]:
        """DeleteUserPipeline method receives a DeleteUserPipelineRequest message and returns
        a DeleteUserPipelineResponse message.
        """
    @abc.abstractmethod
    def ValidateUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ValidateUserPipelineResponse]]:
        """Validate a pipeline."""
    @abc.abstractmethod
    def RenameUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineResponse]]:
        """RenameUserPipeline method receives a RenameUserPipelineRequest message and returns
        a RenameUserPipelineResponse message.
        """
    @abc.abstractmethod
    def TriggerUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineResponse]]:
        """TriggerUserPipeline method receives a TriggerUserPipelineRequest message
        and returns a TriggerUserPipelineResponse.
        """
    @abc.abstractmethod
    def TriggerAsyncUserPipeline(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineResponse]]:
        """TriggerAsyncUserPipeline method receives a TriggerAsyncUserPipelineRequest message and
        returns a TriggerAsyncUserPipelineResponse.
        """
    @abc.abstractmethod
    def GetOperation(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.GetOperationRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.GetOperationResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.GetOperationResponse]]:
        """*Longrunning operation methods

        GetOperation method receives a
        GetOperationRequest message and returns a
        GetOperationResponse message.
        """
    @abc.abstractmethod
    def CreateUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.CreateUserPipelineReleaseResponse]]:
        """CreateUserPipelineRelease method receives a CreateUserPipelineReleaseRequest message and returns
        a CreateUserPipelineReleaseResponse message.
        """
    @abc.abstractmethod
    def ListUserPipelineReleases(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.ListUserPipelineReleasesResponse]]:
        """ListUserPipelineReleases method receives a ListUserPipelineReleasesRequest message and returns a
        ListUserPipelineReleasesResponse message.
        """
    @abc.abstractmethod
    def GetUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.GetUserPipelineReleaseResponse]]:
        """GetUserPipelineRelease method receives a GetUserPipelineReleaseRequest message and returns a
        GetUserPipelineReleaseResponse message.
        """
    @abc.abstractmethod
    def UpdateUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.UpdateUserPipelineReleaseResponse]]:
        """UpdateUserPipelineRelease method receives a UpdateUserPipelineReleaseRequest message and returns
        a UpdateUserPipelineReleaseResponse message.
        """
    @abc.abstractmethod
    def DeleteUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.DeleteUserPipelineReleaseResponse]]:
        """DeleteUserPipelineRelease method receives a DeleteUserPipelineReleaseRequest message and returns
        a DeleteUserPipelineReleaseResponse message.
        """
    @abc.abstractmethod
    def RestoreUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.RestoreUserPipelineReleaseResponse]]:
        """RestoreUserPipelineRelease method receives a RestoreUserPipelineReleaseRequest message
        and returns a RestoreUserPipelineReleaseResponse
        """
    @abc.abstractmethod
    def SetDefaultUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.SetDefaultUserPipelineReleaseResponse]]:
        """SetDefaultUserPipelineRelease method receives a SetDefaultUserPipelineReleaseRequest message
        and returns a SetDefaultUserPipelineReleaseResponse
        """
    @abc.abstractmethod
    def WatchUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.WatchUserPipelineReleaseResponse]]:
        """WatchUserPipelineRelease method receives a WatchUserPipelineReleaseRequest message
        and returns a WatchUserPipelineReleaseResponse
        """
    @abc.abstractmethod
    def RenameUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.RenameUserPipelineReleaseResponse]]:
        """RenameUserPipelineRelease method receives a RenameUserPipelineReleaseRequest message and returns
        a RenameUserPipelineReleaseResponse message.
        """
    @abc.abstractmethod
    def TriggerUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.TriggerUserPipelineReleaseResponse]]:
        """TriggerUserPipelineRelease method receives a TriggeUserPipelineReleaseRequest message
        and returns a TriggerPipelineReleasePipelineResponse.
        """
    @abc.abstractmethod
    def TriggerAsyncUserPipelineRelease(
        self,
        request: vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseResponse, collections.abc.Awaitable[vdp.pipeline.v1alpha.pipeline_pb2.TriggerAsyncUserPipelineReleaseResponse]]:
        """TriggerAsyncUserPipelineRelease method receives a TriggerAsyncUserPipelineReleaseRequest message and
        returns a TriggerAsyncUserPipelineReleaseResponse.
        """

def add_PipelinePublicServiceServicer_to_server(servicer: PipelinePublicServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...

"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import base.mgmt.v1alpha.metric_pb2
import base.mgmt.v1alpha.mgmt_pb2
import collections.abc
import grpc
import grpc.aio
import typing

_T = typing.TypeVar('_T')

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta):
    ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore
    ...

class MgmtPublicServiceStub:
    """Mgmt service responds to external access"""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Liveness: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.LivenessRequest,
        base.mgmt.v1alpha.mgmt_pb2.LivenessResponse,
    ]
    """Liveness method receives a LivenessRequest message and returns a
    LivenessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    Readiness: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ReadinessRequest,
        base.mgmt.v1alpha.mgmt_pb2.ReadinessResponse,
    ]
    """Readiness method receives a ReadinessRequest message and returns a
    ReadinessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    QueryAuthenticatedUser: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserRequest,
        base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserResponse,
    ]
    """QueryAuthenticatedUser method receives a QueryAuthenticatedUserRequest
    message and returns a QueryAuthenticatedUserResponse message.
    """
    PatchAuthenticatedUser: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserRequest,
        base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserResponse,
    ]
    """PatchAuthenticatedUser method receives a PatchAuthenticatedUserRequest
    message and returns a PatchAuthenticatedUserResponse message.
    """
    ExistUsername: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ExistUsernameRequest,
        base.mgmt.v1alpha.mgmt_pb2.ExistUsernameResponse,
    ]
    """ExistUsername method receives a ExistUsernameRequest message and returns a
    ExistUsernameResponse
    """
    CreateToken: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.CreateTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.CreateTokenResponse,
    ]
    """CreateToken method receives a CreateTokenRequest message and returns
    a CreateTokenResponse message.
    """
    ListTokens: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ListTokensRequest,
        base.mgmt.v1alpha.mgmt_pb2.ListTokensResponse,
    ]
    """ListTokens method receives a ListTokensRequest message and returns a
    ListTokensResponse message.
    """
    GetToken: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.GetTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.GetTokenResponse,
    ]
    """GetToken method receives a GetTokenRequest message and returns a
    GetTokenResponse message.
    """
    DeleteToken: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.DeleteTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.DeleteTokenResponse,
    ]
    """DeleteToken method receives a DeleteTokenRequest message and returns
    a DeleteTokenResponse message.
    """
    ValidateToken: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ValidateTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.ValidateTokenResponse,
    ]
    """ValidateToken method receives a ValidateTokenRequest message and returns
    a ValidateTokenResponse message.
    """
    ListPipelineTriggerRecords: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsResponse,
    ]
    """========== Metric endpoints

    ListPipelineTriggerRecords method receives a ListPipelineTriggerRecordsRequest message and returns a
    ListPipelineTriggerRecordsResponse message.
    """
    ListPipelineTriggerTableRecords: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsResponse,
    ]
    """ListPipelineTriggerTableRecords method receives a ListPipelineTriggerTableRecordsRequest message and returns a
    ListPipelineTriggerTableRecordsResponse message.
    """
    ListPipelineTriggerChartRecords: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsResponse,
    ]
    """ListPipelineTriggerChartRecords method receives a ListPipelineTriggerChartRecordsRequest message and returns a
    ListPipelineTriggerChartRecordsResponse message.
    """
    ListConnectorExecuteRecords: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsResponse,
    ]
    """ListConnectorExecuteRecords method receives a ListConnectorExecuteRecordsRequest message and returns a
    ListConnectorExecuteRecordsResponse message.
    """
    ListConnectorExecuteTableRecords: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsResponse,
    ]
    """ListConnectorExecuteTableRecords method receives a ListConnectorExecuteTableRecordsRequest message and returns a
    ListConnectorExecuteTableRecordsResponse message.
    """
    ListConnectorExecuteChartRecords: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsResponse,
    ]
    """ListConnectorExecuteChartRecords method receives a ListConnectorExecuteChartRecordsRequest message and returns a
    ListConnectorExecuteChartRecordsResponse message.
    """
    AuthTokenIssuer: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerResponse,
    ]
    """AuthTokenIssuer endpoint"""
    AuthLogin: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthLoginRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthLoginResponse,
    ]
    """Auth Login endpoint"""
    AuthLogout: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthLogoutRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthLogoutResponse,
    ]
    """Auth Logout endpoint"""
    AuthChangePassword: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordResponse,
    ]
    """Auth Change password endpoint"""
    AuthValidateAccessToken: grpc.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenResponse,
    ]
    """Auth AccessToken validation endpoint"""

class MgmtPublicServiceAsyncStub:
    """Mgmt service responds to external access"""

    Liveness: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.LivenessRequest,
        base.mgmt.v1alpha.mgmt_pb2.LivenessResponse,
    ]
    """Liveness method receives a LivenessRequest message and returns a
    LivenessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    Readiness: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ReadinessRequest,
        base.mgmt.v1alpha.mgmt_pb2.ReadinessResponse,
    ]
    """Readiness method receives a ReadinessRequest message and returns a
    ReadinessResponse message.
    See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    """
    QueryAuthenticatedUser: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserRequest,
        base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserResponse,
    ]
    """QueryAuthenticatedUser method receives a QueryAuthenticatedUserRequest
    message and returns a QueryAuthenticatedUserResponse message.
    """
    PatchAuthenticatedUser: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserRequest,
        base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserResponse,
    ]
    """PatchAuthenticatedUser method receives a PatchAuthenticatedUserRequest
    message and returns a PatchAuthenticatedUserResponse message.
    """
    ExistUsername: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ExistUsernameRequest,
        base.mgmt.v1alpha.mgmt_pb2.ExistUsernameResponse,
    ]
    """ExistUsername method receives a ExistUsernameRequest message and returns a
    ExistUsernameResponse
    """
    CreateToken: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.CreateTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.CreateTokenResponse,
    ]
    """CreateToken method receives a CreateTokenRequest message and returns
    a CreateTokenResponse message.
    """
    ListTokens: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ListTokensRequest,
        base.mgmt.v1alpha.mgmt_pb2.ListTokensResponse,
    ]
    """ListTokens method receives a ListTokensRequest message and returns a
    ListTokensResponse message.
    """
    GetToken: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.GetTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.GetTokenResponse,
    ]
    """GetToken method receives a GetTokenRequest message and returns a
    GetTokenResponse message.
    """
    DeleteToken: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.DeleteTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.DeleteTokenResponse,
    ]
    """DeleteToken method receives a DeleteTokenRequest message and returns
    a DeleteTokenResponse message.
    """
    ValidateToken: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.ValidateTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.ValidateTokenResponse,
    ]
    """ValidateToken method receives a ValidateTokenRequest message and returns
    a ValidateTokenResponse message.
    """
    ListPipelineTriggerRecords: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsResponse,
    ]
    """========== Metric endpoints

    ListPipelineTriggerRecords method receives a ListPipelineTriggerRecordsRequest message and returns a
    ListPipelineTriggerRecordsResponse message.
    """
    ListPipelineTriggerTableRecords: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsResponse,
    ]
    """ListPipelineTriggerTableRecords method receives a ListPipelineTriggerTableRecordsRequest message and returns a
    ListPipelineTriggerTableRecordsResponse message.
    """
    ListPipelineTriggerChartRecords: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsResponse,
    ]
    """ListPipelineTriggerChartRecords method receives a ListPipelineTriggerChartRecordsRequest message and returns a
    ListPipelineTriggerChartRecordsResponse message.
    """
    ListConnectorExecuteRecords: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsResponse,
    ]
    """ListConnectorExecuteRecords method receives a ListConnectorExecuteRecordsRequest message and returns a
    ListConnectorExecuteRecordsResponse message.
    """
    ListConnectorExecuteTableRecords: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsResponse,
    ]
    """ListConnectorExecuteTableRecords method receives a ListConnectorExecuteTableRecordsRequest message and returns a
    ListConnectorExecuteTableRecordsResponse message.
    """
    ListConnectorExecuteChartRecords: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsRequest,
        base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsResponse,
    ]
    """ListConnectorExecuteChartRecords method receives a ListConnectorExecuteChartRecordsRequest message and returns a
    ListConnectorExecuteChartRecordsResponse message.
    """
    AuthTokenIssuer: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerResponse,
    ]
    """AuthTokenIssuer endpoint"""
    AuthLogin: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthLoginRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthLoginResponse,
    ]
    """Auth Login endpoint"""
    AuthLogout: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthLogoutRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthLogoutResponse,
    ]
    """Auth Logout endpoint"""
    AuthChangePassword: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordResponse,
    ]
    """Auth Change password endpoint"""
    AuthValidateAccessToken: grpc.aio.UnaryUnaryMultiCallable[
        base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenRequest,
        base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenResponse,
    ]
    """Auth AccessToken validation endpoint"""

class MgmtPublicServiceServicer(metaclass=abc.ABCMeta):
    """Mgmt service responds to external access"""

    @abc.abstractmethod
    def Liveness(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.LivenessRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.LivenessResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.LivenessResponse]]:
        """Liveness method receives a LivenessRequest message and returns a
        LivenessResponse message.
        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
    @abc.abstractmethod
    def Readiness(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.ReadinessRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.ReadinessResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.ReadinessResponse]]:
        """Readiness method receives a ReadinessRequest message and returns a
        ReadinessResponse message.
        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
    @abc.abstractmethod
    def QueryAuthenticatedUser(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.QueryAuthenticatedUserResponse]]:
        """QueryAuthenticatedUser method receives a QueryAuthenticatedUserRequest
        message and returns a QueryAuthenticatedUserResponse message.
        """
    @abc.abstractmethod
    def PatchAuthenticatedUser(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.PatchAuthenticatedUserResponse]]:
        """PatchAuthenticatedUser method receives a PatchAuthenticatedUserRequest
        message and returns a PatchAuthenticatedUserResponse message.
        """
    @abc.abstractmethod
    def ExistUsername(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.ExistUsernameRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.ExistUsernameResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.ExistUsernameResponse]]:
        """ExistUsername method receives a ExistUsernameRequest message and returns a
        ExistUsernameResponse
        """
    @abc.abstractmethod
    def CreateToken(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.CreateTokenRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.CreateTokenResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.CreateTokenResponse]]:
        """CreateToken method receives a CreateTokenRequest message and returns
        a CreateTokenResponse message.
        """
    @abc.abstractmethod
    def ListTokens(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.ListTokensRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.ListTokensResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.ListTokensResponse]]:
        """ListTokens method receives a ListTokensRequest message and returns a
        ListTokensResponse message.
        """
    @abc.abstractmethod
    def GetToken(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.GetTokenRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.GetTokenResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.GetTokenResponse]]:
        """GetToken method receives a GetTokenRequest message and returns a
        GetTokenResponse message.
        """
    @abc.abstractmethod
    def DeleteToken(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.DeleteTokenRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.DeleteTokenResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.DeleteTokenResponse]]:
        """DeleteToken method receives a DeleteTokenRequest message and returns
        a DeleteTokenResponse message.
        """
    @abc.abstractmethod
    def ValidateToken(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.ValidateTokenRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.ValidateTokenResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.ValidateTokenResponse]]:
        """ValidateToken method receives a ValidateTokenRequest message and returns
        a ValidateTokenResponse message.
        """
    @abc.abstractmethod
    def ListPipelineTriggerRecords(
        self,
        request: base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsResponse, collections.abc.Awaitable[base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerRecordsResponse]]:
        """========== Metric endpoints

        ListPipelineTriggerRecords method receives a ListPipelineTriggerRecordsRequest message and returns a
        ListPipelineTriggerRecordsResponse message.
        """
    @abc.abstractmethod
    def ListPipelineTriggerTableRecords(
        self,
        request: base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsResponse, collections.abc.Awaitable[base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerTableRecordsResponse]]:
        """ListPipelineTriggerTableRecords method receives a ListPipelineTriggerTableRecordsRequest message and returns a
        ListPipelineTriggerTableRecordsResponse message.
        """
    @abc.abstractmethod
    def ListPipelineTriggerChartRecords(
        self,
        request: base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsResponse, collections.abc.Awaitable[base.mgmt.v1alpha.metric_pb2.ListPipelineTriggerChartRecordsResponse]]:
        """ListPipelineTriggerChartRecords method receives a ListPipelineTriggerChartRecordsRequest message and returns a
        ListPipelineTriggerChartRecordsResponse message.
        """
    @abc.abstractmethod
    def ListConnectorExecuteRecords(
        self,
        request: base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsResponse, collections.abc.Awaitable[base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteRecordsResponse]]:
        """ListConnectorExecuteRecords method receives a ListConnectorExecuteRecordsRequest message and returns a
        ListConnectorExecuteRecordsResponse message.
        """
    @abc.abstractmethod
    def ListConnectorExecuteTableRecords(
        self,
        request: base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsResponse, collections.abc.Awaitable[base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteTableRecordsResponse]]:
        """ListConnectorExecuteTableRecords method receives a ListConnectorExecuteTableRecordsRequest message and returns a
        ListConnectorExecuteTableRecordsResponse message.
        """
    @abc.abstractmethod
    def ListConnectorExecuteChartRecords(
        self,
        request: base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsResponse, collections.abc.Awaitable[base.mgmt.v1alpha.metric_pb2.ListConnectorExecuteChartRecordsResponse]]:
        """ListConnectorExecuteChartRecords method receives a ListConnectorExecuteChartRecordsRequest message and returns a
        ListConnectorExecuteChartRecordsResponse message.
        """
    @abc.abstractmethod
    def AuthTokenIssuer(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.AuthTokenIssuerResponse]]:
        """AuthTokenIssuer endpoint"""
    @abc.abstractmethod
    def AuthLogin(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.AuthLoginRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.AuthLoginResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.AuthLoginResponse]]:
        """Auth Login endpoint"""
    @abc.abstractmethod
    def AuthLogout(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.AuthLogoutRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.AuthLogoutResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.AuthLogoutResponse]]:
        """Auth Logout endpoint"""
    @abc.abstractmethod
    def AuthChangePassword(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.AuthChangePasswordResponse]]:
        """Auth Change password endpoint"""
    @abc.abstractmethod
    def AuthValidateAccessToken(
        self,
        request: base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenRequest,
        context: _ServicerContext,
    ) -> typing.Union[base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenResponse, collections.abc.Awaitable[base.mgmt.v1alpha.mgmt_pb2.AuthValidateAccessTokenResponse]]:
        """Auth AccessToken validation endpoint"""

def add_MgmtPublicServiceServicer_to_server(servicer: MgmtPublicServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...

# pylint: disable=no-member,wrong-import-position
from datetime import datetime
from typing import List

# common
from google.protobuf import field_mask_pb2, timestamp_pb2

import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck

# mgmt
import instill.protogen.core.mgmt.v1beta.metric_pb2 as metric_interface
import instill.protogen.core.mgmt.v1beta.mgmt_pb2 as mgmt_interface
import instill.protogen.core.mgmt.v1beta.mgmt_public_service_pb2_grpc as mgmt_service
from instill.clients.base import Client, RequestFactory
from instill.clients.instance import InstillInstance
from instill.helpers.const import HOST_URL_PROD
from instill.utils.error_handler import grpc_handler


class MgmtClient(Client):
    def __init__(
        self,
        api_token: str,
        url: str = HOST_URL_PROD,
        secure: bool = True,
        requester_id: str = "",
        async_enabled: bool = False,
    ) -> None:

        self.host: InstillInstance = InstillInstance(
            mgmt_service.MgmtPublicServiceStub,
            url=url,
            token=api_token,
            secure=secure,
            async_enabled=async_enabled,
        )

        self.metadata = []

        if requester_id != "":
            requester_uid = self._lookup_namespace_uid(requester_id)
            self.metadata = [("instill-requester-uid", requester_uid)]

    def close(self):
        if self.is_serving():
            self.host.channel.close()

    async def async_close(self):
        if self.is_serving():
            self.host.channel.close()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host: InstillInstance):
        self._host = host

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: List[tuple]):
        self._metadata = metadata

    def _lookup_namespace_uid(self, namespace_id: str):
        resp = self.check_namespace(namespace_id)
        if resp.type == mgmt_interface.CheckNamespaceAdminResponse.NAMESPACE_USER:
            namespace_uid = self.get_user(namespace_id).user.uid
        elif (
            resp.type
            == mgmt_interface.CheckNamespaceAdminResponse.NAMESPACE_ORGANIZATION
        ):
            namespace_uid = self.get_organization(namespace_id).organization.uid
        else:
            raise Exception("namespace ID not available")

        return namespace_uid

    def liveness(self, async_enabled: bool = False) -> mgmt_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Liveness,
                request=mgmt_interface.LivenessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Liveness,
            request=mgmt_interface.LivenessRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    def readiness(
        self, async_enabled: bool = False
    ) -> mgmt_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Readiness,
                request=mgmt_interface.ReadinessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Readiness,
            request=mgmt_interface.ReadinessRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    def is_serving(self) -> bool:
        try:
            return (
                self.readiness().health_check_response.status
                == healthcheck.HealthCheckResponse.SERVING_STATUS_SERVING
            )
        except Exception:
            return False

    @grpc_handler
    def check_namespace(
        self,
        namespace: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.CheckNamespaceResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CheckNamespace,
                request=mgmt_interface.CheckNamespaceRequest(id=namespace),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CheckNamespace,
            request=mgmt_interface.CheckNamespaceRequest(id=namespace),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_user_membership(
        self,
        user_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListUserMembershipsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListUserMemberships,
                request=mgmt_interface.ListUserMembershipsRequest(
                    user_id=user_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListUserMemberships,
            request=mgmt_interface.ListUserMembershipsRequest(
                user_id=user_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_user_membership(
        self,
        user_id: str,
        organization_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetUserMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetUserMembership,
                request=mgmt_interface.GetUserMembershipRequest(
                    view=mgmt_interface.VIEW_FULL,
                    user_id=user_id,
                    organization_id=organization_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetUserMembership,
            request=mgmt_interface.GetUserMembershipRequest(
                view=mgmt_interface.VIEW_FULL,
                user_id=user_id,
                organization_id=organization_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_user_membership(
        self,
        membership: mgmt_interface.UserMembership,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> mgmt_interface.UpdateUserMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateUserMembership,
                request=mgmt_interface.UpdateUserMembershipRequest(
                    membership=membership,
                    update_mask=mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.UpdateUserMembership,
            request=mgmt_interface.UpdateUserMembershipRequest(
                membership=membership,
                update_mask=mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_user_membership(
        self,
        user_id: str,
        organization_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteUserMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteUserMembership,
                request=mgmt_interface.DeleteUserMembershipRequest(
                    user_id=user_id,
                    organization_id=organization_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteUserMembership,
            request=mgmt_interface.DeleteUserMembershipRequest(
                user_id=user_id,
                organization_id=organization_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_organization(
        self,
        organization: mgmt_interface.Organization,
        async_enabled: bool = False,
    ) -> mgmt_interface.CreateOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateOrganization,
                request=mgmt_interface.CreateOrganizationRequest(
                    organization=organization
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.CreateOrganization,
            request=mgmt_interface.CreateOrganizationRequest(organization=organization),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_organization(
        self,
        filter_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListOrganizationsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListOrganizations,
                request=mgmt_interface.ListOrganizationsRequest(
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    view=mgmt_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.ListOrganizations,
            request=mgmt_interface.ListOrganizationsRequest(
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                view=mgmt_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_organization(
        self,
        organization_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetOrganization,
                request=mgmt_interface.GetOrganizationRequest(
                    view=mgmt_interface.VIEW_FULL,
                    organization_id=organization_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetOrganization,
            request=mgmt_interface.GetOrganizationRequest(
                view=mgmt_interface.VIEW_FULL,
                organization_id=organization_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_organization(
        self,
        organization: mgmt_interface.Organization,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> mgmt_interface.UpdateOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateOrganization,
                request=mgmt_interface.UpdateOrganizationRequest(
                    organization=organization,
                    update_mask=mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.UpdateOrganization,
            request=mgmt_interface.UpdateOrganizationRequest(
                organization=organization,
                update_mask=mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_organization(
        self,
        organization_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteOrganization,
                request=mgmt_interface.DeleteOrganizationRequest(
                    organization_id=organization_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteOrganization,
            request=mgmt_interface.DeleteOrganizationRequest(
                organization_id=organization_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_organization_memberships(
        self,
        organization_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListOrganizationMembershipsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListOrganizationMemberships,
                request=mgmt_interface.ListOrganizationMembershipsRequest(
                    organization_id=organization_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListOrganizationMemberships,
            request=mgmt_interface.ListOrganizationMembershipsRequest(
                organization_id=organization_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_organization_membership(
        self,
        organization_id: str,
        user_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetOrganizationMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetOrganizationMembership,
                request=mgmt_interface.GetOrganizationMembershipRequest(
                    view=mgmt_interface.VIEW_FULL,
                    organization_id=organization_id,
                    user_id=user_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetOrganizationMembership,
            request=mgmt_interface.GetOrganizationMembershipRequest(
                view=mgmt_interface.VIEW_FULL,
                organization_id=organization_id,
                user_id=user_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_organization_membership(
        self,
        membership: mgmt_interface.OrganizationMembership,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> mgmt_interface.UpdateOrganizationMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateOrganizationMembership,
                request=mgmt_interface.UpdateOrganizationMembershipRequest(
                    membership=membership,
                    update_mask=mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.UpdateOrganizationMembership,
            request=mgmt_interface.UpdateOrganizationMembershipRequest(
                membership=membership,
                update_mask=mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_organization_membership(
        self,
        organization_id: str,
        user_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteOrganizationMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteOrganizationMembership,
                request=mgmt_interface.DeleteOrganizationMembershipRequest(
                    organization_id=organization_id,
                    user_id=user_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteOrganizationMembership,
            request=mgmt_interface.DeleteOrganizationMembershipRequest(
                organization_id=organization_id,
                user_id=user_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def login(
        self,
        username="admin",
        password="password",
        async_enabled: bool = False,
    ) -> mgmt_interface.AuthLoginResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.AuthLogin,
                request=mgmt_interface.AuthLoginRequest(
                    username=username, password=password
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.AuthLogin,
            request=mgmt_interface.AuthLoginRequest(
                username=username, password=password
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_token(
        self,
        token: mgmt_interface.ApiToken,
        async_enabled: bool = False,
    ) -> mgmt_interface.CreateTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateToken,
                request=mgmt_interface.CreateTokenRequest(token=token),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateToken,
            request=mgmt_interface.CreateTokenRequest(token=token),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_token(
        self,
        token_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetToken,
                request=mgmt_interface.GetTokenRequest(
                    token_id=token_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetToken,
            request=mgmt_interface.GetTokenRequest(
                token_id=token_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_tokens(
        self,
        next_page_token: str = "",
        total_size: int = 100,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListTokensResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListTokens,
                request=mgmt_interface.ListTokensRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListTokens,
            request=mgmt_interface.ListTokensRequest(
                page_size=total_size,
                page_token=next_page_token,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_token(
        self,
        token_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteToken,
                request=mgmt_interface.DeleteTokenRequest(
                    token_id=token_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteToken,
            request=mgmt_interface.DeleteTokenRequest(
                token_id=token_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def validate_token(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.ValidateTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ValidateToken,
                request=mgmt_interface.ValidateTokenRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ValidateToken,
            request=mgmt_interface.ValidateTokenRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_user(
        self,
        user_id: str = "me",
        async_enabled: bool = False,
    ) -> mgmt_interface.GetUserResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetUser,
                request=mgmt_interface.GetUserRequest(
                    view=mgmt_interface.VIEW_FULL,
                    user_id=user_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetUser,
            request=mgmt_interface.GetUserRequest(
                view=mgmt_interface.VIEW_FULL,
                user_id=user_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_remaining_credit(
        self,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetRemainingCreditResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetRemainingCredit,
                request=mgmt_interface.GetRemainingCreditRequest(
                    namespace_id=namespace_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetRemainingCredit,
            request=mgmt_interface.GetRemainingCreditRequest(
                namespace_id=namespace_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_trigger_records(
        self,
        total_size: int = 10,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> metric_interface.ListPipelineTriggerRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListPipelineTriggerRecords,
                request=metric_interface.ListPipelineTriggerRecordsRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListPipelineTriggerRecords,
            request=metric_interface.ListPipelineTriggerRecordsRequest(
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_pipeline_trigger_count(
        self,
        namespace_id: str,
        start: datetime,
        stop: datetime,
        async_enabled: bool = False,
    ) -> metric_interface.GetPipelineTriggerCountResponse:
        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start)
        stop_timestamp = timestamp_pb2.Timestamp()
        stop_timestamp.FromDatetime(stop)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetPipelineTriggerCount,
                request=metric_interface.GetPipelineTriggerCountRequest(
                    namespace_id=namespace_id,
                    start=start_timestamp,
                    stop=stop_timestamp,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetPipelineTriggerCount,
            request=metric_interface.GetPipelineTriggerCountRequest(
                namespace_id=namespace_id,
                start=start_timestamp,
                stop=stop_timestamp,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_model_trigger_count(
        self,
        requester_id: str,
        start: datetime,
        stop: datetime,
        async_enabled: bool = False,
    ) -> metric_interface.GetModelTriggerCountResponse:
        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start)
        stop_timestamp = timestamp_pb2.Timestamp()
        stop_timestamp.FromDatetime(stop)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetModelTriggerCount,
                request=metric_interface.GetModelTriggerCountRequest(
                    requester_id=requester_id,
                    start=start_timestamp,
                    stop=stop_timestamp,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetModelTriggerCount,
            request=metric_interface.GetModelTriggerCountRequest(
                requester_id=requester_id,
                start=start_timestamp,
                stop=stop_timestamp,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_trigger_table_records(
        self,
        total_size: int = 100,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> metric_interface.ListPipelineTriggerTableRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListPipelineTriggerTableRecords,
                request=metric_interface.ListPipelineTriggerTableRecordsRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListPipelineTriggerTableRecords,
            request=metric_interface.ListPipelineTriggerTableRecordsRequest(
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_trigger_chart_records(
        self,
        aggregation_window: int,
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> metric_interface.ListPipelineTriggerChartRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListPipelineTriggerChartRecords,
                request=metric_interface.ListPipelineTriggerChartRecordsRequest(
                    aggregation_window=aggregation_window,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListPipelineTriggerChartRecords,
            request=metric_interface.ListPipelineTriggerChartRecordsRequest(
                aggregation_window=aggregation_window,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_authenticated_user(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetAuthenticatedUserResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetAuthenticatedUser,
                request=mgmt_interface.GetAuthenticatedUserRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetAuthenticatedUser,
            request=mgmt_interface.GetAuthenticatedUserRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def patch_authenticated_user(
        self,
        user: mgmt_interface.AuthenticatedUser,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> mgmt_interface.PatchAuthenticatedUserResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.PatchAuthenticatedUser,
                request=mgmt_interface.PatchAuthenticatedUserRequest(
                    user=user,
                    update_mask=mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.PatchAuthenticatedUser,
            request=mgmt_interface.PatchAuthenticatedUserRequest(
                user=user,
                update_mask=mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_users(
        self,
        total_size: int = 100,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> mgmt_interface.ListUsersResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListUsers,
                request=mgmt_interface.ListUsersRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                    view=mgmt_interface.VIEW_FULL,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListUsers,
            request=mgmt_interface.ListUsersRequest(
                page_size=total_size,
                page_token=next_page_token,
                view=mgmt_interface.VIEW_FULL,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_authenticated_subscription(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetAuthenticatedUserSubscriptionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetAuthenticatedUserSubscription,
                request=mgmt_interface.GetAuthenticatedUserSubscriptionRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetAuthenticatedUserSubscription,
            request=mgmt_interface.GetAuthenticatedUserSubscriptionRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_organization_subscription(
        self,
        organization_id: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetOrganizationSubscriptionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetOrganizationSubscription,
                request=mgmt_interface.GetOrganizationSubscriptionRequest(
                    organization_id=organization_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetOrganizationSubscription,
            request=mgmt_interface.GetOrganizationSubscriptionRequest(
                organization_id=organization_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_credit_consumption_chart_records(
        self,
        namespace_id: str,
        aggregation_window: str,
        start: datetime,
        stop: datetime,
        async_enabled: bool = False,
    ) -> metric_interface.ListCreditConsumptionChartRecordsResponse:
        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start)
        stop_timestamp = timestamp_pb2.Timestamp()
        stop_timestamp.FromDatetime(stop)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListCreditConsumptionChartRecords,
                request=metric_interface.ListCreditConsumptionChartRecordsRequest(
                    namespace_id=namespace_id,
                    aggregation_window=aggregation_window,
                    start=start_timestamp,
                    stop=stop_timestamp,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListCreditConsumptionChartRecords,
            request=metric_interface.ListCreditConsumptionChartRecordsRequest(
                namespace_id=namespace_id,
                aggregation_window=aggregation_window,
                start=start_timestamp,
                stop=stop_timestamp,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def auth_token_issuer(
        self,
        username: str,
        password: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.AuthTokenIssuerResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.AuthTokenIssuer,
                request=mgmt_interface.AuthTokenIssuerRequest(
                    username=username,
                    password=password,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.AuthTokenIssuer,
            request=mgmt_interface.AuthTokenIssuerRequest(
                username=username,
                password=password,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def auth_logout(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.AuthLogoutResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.AuthLogout,
                request=mgmt_interface.AuthLogoutRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.AuthLogout,
            request=mgmt_interface.AuthLogoutRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def auth_change_password(
        self,
        old_password: str,
        new_password: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.AuthChangePasswordResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.AuthChangePassword,
                request=mgmt_interface.AuthChangePasswordRequest(
                    old_password=old_password,
                    new_password=new_password,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.AuthChangePassword,
            request=mgmt_interface.AuthChangePasswordRequest(
                old_password=old_password,
                new_password=new_password,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def auth_validate_access_token(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.AuthValidateAccessTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.AuthValidateAccessToken,
                request=mgmt_interface.AuthValidateAccessTokenRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.AuthValidateAccessToken,
            request=mgmt_interface.AuthValidateAccessTokenRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

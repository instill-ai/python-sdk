# pylint: disable=no-member,wrong-import-position
from typing import Dict

# common
from google.protobuf import field_mask_pb2

import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck

# mgmt
import instill.protogen.core.mgmt.v1beta.metric_pb2 as metric_interface
import instill.protogen.core.mgmt.v1beta.mgmt_pb2 as mgmt_interface
import instill.protogen.core.mgmt.v1beta.mgmt_public_service_pb2_grpc as mgmt_service
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler

# from instill.utils.logger import Logger


class MgmtClient(Client):
    def __init__(self, async_enabled: bool) -> None:
        self.hosts: Dict[str, InstillInstance] = {}
        if DEFAULT_INSTANCE in global_config.hosts:
            self.instance = DEFAULT_INSTANCE
        elif len(global_config.hosts) == 0:
            self.instance = ""
        else:
            self.instance = list(global_config.hosts.keys())[0]

        if global_config.hosts is not None:
            for instance, config in global_config.hosts.items():
                self.hosts[instance] = InstillInstance(
                    mgmt_service.MgmtPublicServiceStub,
                    url=config.url,
                    token=config.token,
                    secure=config.secure,
                    async_enabled=async_enabled,
                )

    @property
    def hosts(self):
        return self._hosts

    @hosts.setter
    def hosts(self, hosts: str):
        self._hosts = hosts

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, instance: str):
        self._instance = instance

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: str):
        self._metadata = metadata

    def liveness(self, async_enabled: bool = False) -> mgmt_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Liveness,
                request=mgmt_interface.LivenessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Liveness,
            request=mgmt_interface.LivenessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    def readiness(
        self, async_enabled: bool = False
    ) -> mgmt_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Readiness,
                request=mgmt_interface.ReadinessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Readiness,
            request=mgmt_interface.ReadinessRequest(),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.CheckNamespace,
                request=mgmt_interface.CheckNamespaceRequest(id=namespace),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CheckNamespace,
            request=mgmt_interface.CheckNamespaceRequest(id=namespace),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_user_membership(
        self,
        parent: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListUserMembershipsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListUserMemberships,
                request=mgmt_interface.ListUserMembershipsRequest(parent=parent),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListUserMemberships,
            request=mgmt_interface.ListUserMembershipsRequest(parent=parent),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_user_membership(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetUserMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserMembership,
                request=mgmt_interface.GetUserMembershipRequest(
                    name=name,
                    view=mgmt_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserMembership,
            request=mgmt_interface.GetUserMembershipRequest(
                name=name,
                view=mgmt_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.UpdateUserMembership,
                request=mgmt_interface.UpdateUserMembershipRequest(
                    membership=membership,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserMembership,
            request=mgmt_interface.UpdateUserMembershipRequest(
                membership=membership,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_user_membership(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteUserMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserMembership,
                request=mgmt_interface.DeleteUserMembershipRequest(name=name),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserMembership,
            request=mgmt_interface.DeleteUserMembershipRequest(name=name),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_organization(
        self,
        organization: mgmt_interface.Organization,
        async_enabled: bool = False,
    ) -> mgmt_interface.CreateOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateOrganization,
                request=mgmt_interface.CreateOrganizationRequest(
                    organization=organization
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.CreateOrganization,
            request=mgmt_interface.CreateOrganizationRequest(organization=organization),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_organization(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListOrganizationsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOrganizations,
                request=mgmt_interface.ListOrganizationsRequest(
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    view=mgmt_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizations,
            request=mgmt_interface.ListOrganizationsRequest(
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                view=mgmt_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_organization(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganization,
                request=mgmt_interface.GetOrganizationRequest(
                    name=name,
                    view=mgmt_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganization,
            request=mgmt_interface.GetOrganizationRequest(
                name=name,
                view=mgmt_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.UpdateOrganization,
                request=mgmt_interface.UpdateOrganizationRequest(
                    organization=organization,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganization,
            request=mgmt_interface.UpdateOrganizationRequest(
                organization=organization,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_organization(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteOrganization,
                request=mgmt_interface.DeleteOrganizationRequest(name=name),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganization,
            request=mgmt_interface.DeleteOrganizationRequest(name=name),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_organization_memberships(
        self,
        parent: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.ListOrganizationMembershipsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListOrganizationMemberships,
                request=mgmt_interface.ListOrganizationMembershipsRequest(
                    parent=parent
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationMemberships,
            request=mgmt_interface.ListOrganizationMembershipsRequest(parent=parent),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_organization_membership(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetOrganizationMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganizationMembership,
                request=mgmt_interface.GetOrganizationMembershipRequest(
                    name=name,
                    view=mgmt_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationMembership,
            request=mgmt_interface.GetOrganizationMembershipRequest(
                name=name,
                view=mgmt_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_organization_membership(
        self,
        membership: mgmt_interface.OrganizationMembership,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> mgmt_interface.UpdateOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateOrganizationMembership,
                request=mgmt_interface.UpdateOrganizationMembershipRequest(
                    membership=membership,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationMembership,
            request=mgmt_interface.UpdateOrganizationMembershipRequest(
                membership=membership,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_organization_membership(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteOrganizationMembershipResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.DeleteOrganizationMembership,
                request=mgmt_interface.DeleteOrganizationMembershipRequest(name=name),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationMembership,
            request=mgmt_interface.DeleteOrganizationMembershipRequest(name=name),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.AuthLogin,
                request=mgmt_interface.AuthLoginRequest(
                    username=username, password=password
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.AuthLogin,
            request=mgmt_interface.AuthLoginRequest(
                username=username, password=password
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_token(
        self,
        token: mgmt_interface.ApiToken,
        async_enabled: bool = False,
    ) -> mgmt_interface.CreateTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateToken,
                request=mgmt_interface.CreateTokenRequest(token=token),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateToken,
            request=mgmt_interface.CreateTokenRequest(token=token),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_token(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetToken,
                request=mgmt_interface.GetTokenRequest(name=name),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetToken,
            request=mgmt_interface.GetTokenRequest(name=name),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.ListTokens,
                request=mgmt_interface.ListTokensRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListTokens,
            request=mgmt_interface.ListTokensRequest(
                page_size=total_size,
                page_token=next_page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_token(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.DeleteTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteToken,
                request=mgmt_interface.DeleteTokenRequest(name=name),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteToken,
            request=mgmt_interface.DeleteTokenRequest(name=name),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def validate_token(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.ValidateTokenResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ValidateToken,
                request=mgmt_interface.ValidateTokenRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ValidateToken,
            request=mgmt_interface.ValidateTokenRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_user(
        self,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetUserResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUser,
                request=mgmt_interface.GetUserRequest(name="users/me"),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUser,
            request=mgmt_interface.GetUserRequest(name="users/me"),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_remaining_credit(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetRemainingCreditResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetRemainingCredit,
                request=mgmt_interface.GetRemainingCreditRequest(owner=f"users/{name}"),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetRemainingCredit,
            request=mgmt_interface.GetRemainingCreditRequest(owner=f"users/{name}"),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_org(
        self,
        org_name: str,
        async_enabled: bool = False,
    ) -> mgmt_interface.GetOrganizationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganization,
                request=mgmt_interface.GetOrganizationRequest(name=f"orgs/{org_name}"),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganization,
            request=mgmt_interface.GetOrganizationRequest(name=f"orgs/{org_name}"),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_trigger_records(
        self,
        async_enabled: bool = False,
    ) -> metric_interface.ListPipelineTriggerRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListPipelineTriggerRecords,
                request=metric_interface.ListPipelineTriggerChartRecordsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListPipelineTriggerRecords,
            request=metric_interface.ListPipelineTriggerChartRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_trigger_table_records(
        self,
        async_enabled: bool = False,
    ) -> metric_interface.ListPipelineTriggerTableRecordsRequest:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListPipelineTriggerTableRecords,
                request=metric_interface.ListPipelineTriggerTableRecordsResponse(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListPipelineTriggerTableRecords,
            request=metric_interface.ListPipelineTriggerTableRecordsResponse(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_trigger_chart_records(
        self,
        async_enabled: bool = False,
    ) -> metric_interface.ListPipelineTriggerChartRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListPipelineTriggerChartRecords,
                request=metric_interface.ListPipelineTriggerChartRecordsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListPipelineTriggerChartRecords,
            request=metric_interface.ListPipelineTriggerChartRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

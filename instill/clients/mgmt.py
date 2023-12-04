# pylint: disable=no-member,wrong-import-position
from typing import Dict

import instill.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# mgmt
import instill.protogen.core.mgmt.v1alpha.metric_pb2 as metric_interface
import instill.protogen.core.mgmt.v1alpha.mgmt_pb2 as mgmt_interface
import instill.protogen.core.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service

# common
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

    @grpc_handler
    def list_connector_execute_records(
        self,
        async_enabled: bool = False,
    ) -> metric_interface.ListConnectorExecuteRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListConnectorExecuteRecords,
                request=metric_interface.ListConnectorExecuteRecordsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListConnectorExecuteRecords,
            request=metric_interface.ListConnectorExecuteRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_connector_execute_table_records(
        self,
        async_enabled: bool = False,
    ) -> metric_interface.ListConnectorExecuteTableRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListConnectorExecuteTableRecords,
                request=metric_interface.ListConnectorExecuteTableRecordsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListConnectorExecuteTableRecords,
            request=metric_interface.ListConnectorExecuteTableRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_connector_execute_chart_records(
        self,
        async_enabled: bool = False,
    ) -> metric_interface.ListConnectorExecuteChartRecordsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListConnectorExecuteChartRecords,
                request=metric_interface.ListConnectorExecuteChartRecordsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListConnectorExecuteChartRecords,
            request=metric_interface.ListConnectorExecuteChartRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

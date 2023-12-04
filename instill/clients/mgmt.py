# pylint: disable=no-member,wrong-import-position
from typing import Dict

import instill.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# mgmt
import instill.protogen.core.mgmt.v1alpha.metric_pb2 as metric_interface
import instill.protogen.core.mgmt.v1alpha.mgmt_pb2 as mgmt_interface
import instill.protogen.core.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service
from instill.clients.base import Client

# common
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler

# from instill.utils.logger import Logger


class MgmtClient(Client):
    def __init__(self, asyncio: bool) -> None:
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
                    asyncio=asyncio,
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

    def liveness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        resp: mgmt_interface.LivenessResponse = self.hosts[
            self.instance
        ].client.Liveness(request=mgmt_interface.LivenessRequest())
        return resp.health_check_response.status

    def readiness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        resp: mgmt_interface.ReadinessResponse = self.hosts[
            self.instance
        ].client.Readiness(request=mgmt_interface.ReadinessRequest())
        return resp.health_check_response.status

    def is_serving(self) -> bool:
        try:
            return (
                self.readiness()
                == healthcheck.HealthCheckResponse.SERVING_STATUS_SERVING
            )
        except Exception:
            return False

    @grpc_handler
    def login(self, username="admin", password="password") -> str:
        resp: mgmt_interface.AuthLoginResponse = self.hosts[
            self.instance
        ].client.AuthLogin(
            request=mgmt_interface.AuthLoginRequest(
                username=username, password=password
            )
        )
        return resp.access_token

    @grpc_handler
    def get_token(self, name: str) -> mgmt_interface.ApiToken:
        resp: mgmt_interface.GetTokenResponse = self.hosts[
            self.instance
        ].client.GetToken(
            request=mgmt_interface.GetTokenRequest(name=name),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.token

    @grpc_handler
    def get_user(self) -> mgmt_interface.User:
        resp: mgmt_interface.GetUserResponse = self.hosts[self.instance].client.GetUser(
            request=mgmt_interface.GetUserRequest(name="users/me"),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.user

    @grpc_handler
    def list_pipeline_trigger_records(
        self,
    ) -> metric_interface.ListPipelineTriggerRecordsResponse:
        return self.hosts[self.instance].client.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        )

    @grpc_handler
    def list_pipeline_trigger_table_records(
        self,
    ) -> metric_interface.ListPipelineTriggerTableRecordsRequest:
        return self.hosts[self.instance].client.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerTableRecordsResponse(),
            metadata=self.hosts[self.instance].metadata,
        )

    @grpc_handler
    def list_pipeline_trigger_chart_records(
        self,
    ) -> metric_interface.ListPipelineTriggerChartRecordsResponse:
        return self.hosts[self.instance].client.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        )

    @grpc_handler
    def list_connector_execute_records(
        self,
    ) -> metric_interface.ListConnectorExecuteRecordsResponse:
        return self.hosts[self.instance].client.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        )

    @grpc_handler
    def list_connector_execute_table_records(
        self,
    ) -> metric_interface.ListConnectorExecuteTableRecordsResponse:
        return self.hosts[self.instance].client.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteTableRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        )

    @grpc_handler
    def list_connector_execute_chart_records(
        self,
    ) -> metric_interface.ListConnectorExecuteChartRecordsResponse:
        return self.hosts[self.instance].client.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteChartRecordsRequest(),
            metadata=self.hosts[self.instance].metadata,
        )

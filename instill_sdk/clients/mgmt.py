# pylint: disable=no-member,wrong-import-position
from collections import defaultdict

import grpc

import instill_sdk.protogen.base.mgmt.v1alpha.metric_pb2 as metric_interface
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service
import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck
from instill_sdk.clients.base import Client
from instill_sdk.configuration import global_config
from instill_sdk.utils.error_handler import grpc_handler

# from instill_sdk.utils.logger import Logger


class MgmtClient(Client):
    def __init__(self) -> None:
        self.hosts = defaultdict(dict)
        self.instance = "default"

        if global_config.hosts is not None:
            for instance in global_config.hosts.keys():
                if global_config.hosts[instance].token is None:
                    channel = grpc.insecure_channel(global_config.hosts[instance].url)
                else:
                    ssl_creds = grpc.ssl_channel_credentials()
                    call_creds = grpc.access_token_call_credentials(
                        global_config.hosts[instance].token
                    )
                    creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
                    channel = grpc.secure_channel(
                        target=global_config.hosts[instance].url,
                        credentials=creds,
                    )
                self.hosts[instance]["channel"] = channel
                self.hosts[instance]["client"] = mgmt_service.MgmtPublicServiceStub(
                    channel
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

    def liveness(self) -> mgmt_interface.LivenessResponse:
        return self.hosts[self.instance]["client"].Liveness(
            request=mgmt_interface.LivenessRequest()
        )

    def readiness(self) -> mgmt_interface.ReadinessResponse:
        return self.hosts[self.instance]["client"].Readiness(
            request=mgmt_interface.ReadinessRequest()
        )

    def is_serving(self) -> bool:
        try:
            return (
                self.readiness().health_check_response.status
                == healthcheck.HealthCheckResponse.SERVING_STATUS_SERVING
            )
        except Exception:
            return False

    @grpc_handler
    def get_user(self) -> mgmt_interface.User:
        response = self.hosts[self.instance]["client"].QueryAuthenticatedUser(
            request=mgmt_interface.QueryAuthenticatedUserRequest()
        )
        return response.user

    @grpc_handler
    def list_pipeline_trigger_records(
        self,
    ) -> metric_interface.ListPipelineTriggerRecordsResponse:
        return self.hosts[self.instance]["client"].ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest()
        )

    @grpc_handler
    def list_pipeline_trigger_table_records(
        self,
    ) -> metric_interface.ListPipelineTriggerTableRecordsRequest:
        return self.hosts[self.instance]["client"].ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerTableRecordsResponse()
        )

    @grpc_handler
    def list_pipeline_trigger_chart_records(
        self,
    ) -> metric_interface.ListPipelineTriggerChartRecordsResponse:
        return self.hosts[self.instance]["client"].ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_records(
        self,
    ) -> metric_interface.ListConnectorExecuteRecordsResponse:
        return self.hosts[self.instance]["client"].ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_table_records(
        self,
    ) -> metric_interface.ListConnectorExecuteTableRecordsResponse:
        return self.hosts[self.instance]["client"].ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteTableRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_chart_records(
        self,
    ) -> metric_interface.ListConnectorExecuteChartRecordsResponse:
        return self.hosts[self.instance]["client"].ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteChartRecordsRequest()
        )

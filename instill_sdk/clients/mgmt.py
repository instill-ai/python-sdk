# pylint: disable=no-member,wrong-import-position
import grpc

import instill_sdk.protogen.base.mgmt.v1alpha.metric_pb2 as metric_interface
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service
import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck
from instill_sdk.clients.client import Client
from instill_sdk.utils.error_handler import grpc_handler

# from instill_sdk.utils.logger import Logger


class MgmtClient(Client):
    def __init__(self, protocol="http", host="localhost", port="7080") -> None:
        """Initialize client for management service with target host.

        Args:
            protocol (str): http/https
            host (str): host url
            port (str): host port
        """

        self.protocol = protocol
        self.host = host
        self.port = port

        self._channel = grpc.insecure_channel(
            f"{host}:{port}".format(protocol=protocol, host=host, port=port)
        )
        self._stub = mgmt_service.MgmtPublicServiceStub(self._channel)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        self._protocol = protocol

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host: str):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port: str):
        self._port = port

    @grpc_handler
    def liveness(self) -> mgmt_interface.LivenessResponse:
        return self._stub.Liveness(request=mgmt_interface.LivenessRequest())

    @grpc_handler
    def readiness(self) -> mgmt_interface.ReadinessResponse:
        return self._stub.Readiness(request=mgmt_interface.ReadinessRequest())

    @grpc_handler
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
        response = self._stub.QueryAuthenticatedUser(
            request=mgmt_interface.QueryAuthenticatedUserRequest()
        )
        return response.user

    @grpc_handler
    def list_pipeline_trigger_records(
        self,
    ) -> metric_interface.ListPipelineTriggerRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest()
        )

    @grpc_handler
    def list_pipeline_trigger_table_records(
        self,
    ) -> metric_interface.ListPipelineTriggerTableRecordsRequest:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerTableRecordsResponse()
        )

    @grpc_handler
    def list_pipeline_trigger_chart_records(
        self,
    ) -> metric_interface.ListPipelineTriggerChartRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_records(
        self,
    ) -> metric_interface.ListConnectorExecuteRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_table_records(
        self,
    ) -> metric_interface.ListConnectorExecuteTableRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteTableRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_chart_records(
        self,
    ) -> metric_interface.ListConnectorExecuteChartRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteChartRecordsRequest()
        )

# pylint: disable=no-member,wrong-import-position
from typing import Tuple
import grpc

# mgmt
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface

import instill_sdk.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
import instill_sdk.protogen.vdp.connector.v1alpha.connector_public_service_pb2_grpc as connector_service
import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck
from instill_sdk.clients.client import Client
from instill_sdk.utils.error_handler import grpc_handler

# from instill_sdk.utils.logger import Logger


class ConnectorClient(Client):
    def __init__(
        self, user: mgmt_interface.User, protocol="http", host="localhost", port="8080"
    ) -> None:
        """Initialize client for connector service with target host.

        Args:
            protocol (str): http/https
            host (str): host url
            port (str): host port
        """

        self.protocol = protocol
        self.host = host
        self.port = port

        self._user = user
        self._channel = grpc.insecure_channel(
            f"{host}:{port}".format(protocol=protocol, host=host, port=port)
        )
        self._stub = connector_service.ConnectorPublicServiceStub(self._channel)

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
    def liveness(self) -> connector_interface.LivenessResponse:
        return self._stub.Liveness(request=connector_interface.LivenessRequest())

    @grpc_handler
    def readiness(self) -> connector_interface.ReadinessResponse:
        return self._stub.Readiness(request=connector_interface.ReadinessRequest())

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
    def create_connector(
        self,
        name: str,
        definition: str,
        configuration: dict,
    ) -> connector_interface.ConnectorResource:
        connector = connector_interface.ConnectorResource()
        connector.id = name
        connector.connector_definition = definition
        connector.configuration.update(configuration)
        resp = self._stub.CreateUserConnectorResource(
            request=connector_interface.CreateUserConnectorResourceRequest(
                connector_resource=connector, parent=self._user.name
            )
        )

        return resp.connector_resource

    @grpc_handler
    def get_connector(self, name: str) -> connector_interface.ConnectorResource:
        return self._stub.GetUserConnectorResource(
            request=connector_interface.GetUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}"
            ).connector_resource
        )

    @grpc_handler
    def list_connectors(self) -> Tuple[list, str, int]:
        resp = self._stub.ListUserConnectorResources(
            request=connector_interface.ListUserConnectorResourcesRequest(
                parent=self._user.name
            )
        )
        return (resp.connector_resources, resp.next_page_token, resp.total_size)

    @grpc_handler
    def connect_connector(self, name: str) -> connector_interface.ConnectorResource:
        return self._stub.ConnectUserConnectorResource(
            request=connector_interface.ConnectUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}"
            )
        ).connector_resource

    @grpc_handler
    def disconnect_connector(self, name: str) -> connector_interface.ConnectorResource:
        return self._stub.DisconnectUserConnectorResource(
            request=connector_interface.DisconnectUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}"
            )
        ).connector_resource

    @grpc_handler
    def test_connector(self, name: str) -> connector_interface.ConnectorResource.State:
        return self._stub.TestUserConnectorResource(
            request=connector_interface.TestUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}"
            )
        ).state

    @grpc_handler
    def execute_connector(self, name: str, inputs: list) -> list:
        return self._stub.ExecuteUserConnectorResource(
            request=connector_interface.ExecuteUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}", inputs=inputs
            )
        ).outputs

    @grpc_handler
    def watch_connector(self, name: str) -> connector_interface.ConnectorResource.State:
        return self._stub.WatchUserConnectorResource(
            request=connector_interface.WatchUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}"
            )
        ).state

    @grpc_handler
    def delete_connector(self, name: str):
        self._stub.DeleteUserConnectorResource(
            request=connector_interface.DeleteUserConnectorResourceRequest(
                name=f"{self._user.name}/connectors/{name}"
            )
        )

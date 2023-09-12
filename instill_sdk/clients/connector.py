# pylint: disable=no-member,wrong-import-position
import grpc

# mgmt
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface
import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck
import instill_sdk.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
import instill_sdk.protogen.vdp.connector.v1alpha.connector_public_service_pb2_grpc as connector_service
from instill_sdk.clients.client import Client
from instill_sdk.utils.error_handler import grpc_handler

# from instill_sdk.utils.logger import Logger


class ConnectorClient(Client):
    def __init__(
        self, user: mgmt_interface.User, token="", host="localhost", port="8080"
    ) -> None:
        """Initialize client for connector service with target host.

        Args:
            token (str): api token for authentication
            host (str): host url
            port (str): host port
        """

        self.token = token
        self.host = host
        self.port = port

        self._user = user
        if len(token) == 0:
            self._channel = grpc.insecure_channel(f"{host}:{port}")
        else:
            ssl_creds = grpc.ssl_channel_credentials()
            call_creds = grpc.access_token_call_credentials(token)
            creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
            self._channel = grpc.secure_channel(
                target=f"{host}",
                credentials=creds,
            )
        self._stub = connector_service.ConnectorPublicServiceStub(self._channel)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

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
        connector.connector_definition_name = definition
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
                name=f"{self._user.name}/connector-resources/{name}"
            )
        ).connector_resource

    @grpc_handler
    def connect_connector(self, name: str) -> connector_interface.ConnectorResource:
        return self._stub.ConnectUserConnectorResource(
            request=connector_interface.ConnectUserConnectorResourceRequest(
                name=f"{self._user.name}/connector-resources/{name}"
            )
        ).connector_resource

    @grpc_handler
    def disconnect_connector(self, name: str) -> connector_interface.ConnectorResource:
        return self._stub.DisconnectUserConnectorResource(
            request=connector_interface.DisconnectUserConnectorResourceRequest(
                name=f"{self._user.name}/connector-resources/{name}"
            )
        ).connector_resource

    @grpc_handler
    def test_connector(self, name: str) -> connector_interface.ConnectorResource.State:
        return self._stub.TestUserConnectorResource(
            request=connector_interface.TestUserConnectorResourceRequest(
                name=f"{self._user.name}/connector-resources/{name}"
            )
        ).state

    @grpc_handler
    def execute_connector(self, name: str, inputs: list) -> list:
        return self._stub.ExecuteUserConnectorResource(
            request=connector_interface.ExecuteUserConnectorResourceRequest(
                name=f"{self._user.name}/connector-resources/{name}", inputs=inputs
            )
        ).outputs

    @grpc_handler
    def watch_connector(self, name: str) -> connector_interface.ConnectorResource.State:
        return self._stub.WatchUserConnectorResource(
            request=connector_interface.WatchUserConnectorResourceRequest(
                name=f"{self._user.name}/connector-resources/{name}"
            )
        ).state

    @grpc_handler
    def delete_connector(self, name: str):
        self.disconnect_connector(name)
        self._stub.DeleteUserConnectorResource(
            request=connector_interface.DeleteUserConnectorResourceRequest(
                name=f"{self._user.name}/connector-resources/{name}"
            )
        )

    @grpc_handler
    def list_connectors(self) -> list:
        connectors = []
        resp = self._stub.ListUserConnectorResources(
            connector_interface.ListUserConnectorResourcesRequest(
                parent=self._user.name
            )
        )
        connectors.extend(resp.connector_resources)
        while resp.next_page_token != "":
            resp = self._stub.ListUserConnectorResources(
                connector_interface.ListUserConnectorResourcesRequest(
                    parent=self._user.name,
                    page_token=resp.next_page_token,
                )
            )
            connectors.extend(resp.connector_resources)

        return connectors

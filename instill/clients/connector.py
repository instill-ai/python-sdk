# pylint: disable=no-member,wrong-import-position
from collections import defaultdict
from typing import Tuple

import grpc

import instill.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck
import instill.protogen.vdp.connector.v1alpha.connector_definition_pb2 as connector_definition_interface

# connector
import instill.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
import instill.protogen.vdp.connector.v1alpha.connector_public_service_pb2_grpc as connector_service
from instill.clients import constant
from instill.clients.base import Client

# common
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler

# from instill.utils.logger import Logger


class ConnectorClient(Client):
    def __init__(self, namespace: str) -> None:
        self.hosts: defaultdict = defaultdict(dict)
        self.namespace: str = namespace
        if constant.DEFAULT_INSTANCE in global_config.hosts:
            self.instance = constant.DEFAULT_INSTANCE
        elif len(global_config.hosts) == 0:
            self.instance = ""
        else:
            self.instance = list(global_config.hosts.keys())[0]

        if global_config.hosts is not None:
            for instance, config in global_config.hosts.items():
                if not config.secure:
                    channel = grpc.insecure_channel(config.url)
                    self.hosts[instance]["metadata"] = (
                        (
                            "authorization",
                            f"Bearer {config.token}",
                        ),
                    )
                else:
                    ssl_creds = grpc.ssl_channel_credentials()
                    call_creds = grpc.access_token_call_credentials(config.token)
                    creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
                    channel = grpc.secure_channel(
                        target=config.url,
                        credentials=creds,
                    )
                    self.hosts[instance]["metadata"] = ""
                self.hosts[instance]["token"] = config.token
                self.hosts[instance]["channel"] = channel
                self.hosts[instance][
                    "client"
                ] = connector_service.ConnectorPublicServiceStub(channel)

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

    def liveness(self) -> connector_interface.LivenessResponse:
        return self.hosts[self.instance]["client"].Liveness(
            request=connector_interface.LivenessRequest()
        )

    def readiness(self) -> connector_interface.ReadinessResponse:
        return self.hosts[self.instance]["client"].Readiness(
            request=connector_interface.ReadinessRequest()
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
        resp = self.hosts[self.instance]["client"].CreateUserConnectorResource(
            request=connector_interface.CreateUserConnectorResourceRequest(
                connector_resource=connector, parent=self.namespace
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

        return resp.connector_resource

    @grpc_handler
    def get_connector(self, name: str) -> connector_interface.ConnectorResource:
        return (
            self.hosts[self.instance]["client"]
            .GetUserConnectorResource(
                request=connector_interface.GetUserConnectorResourceRequest(
                    name=f"{self.namespace}/connector-resources/{name}",
                    view=connector_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .connector_resource
        )

    @grpc_handler
    def test_connector(self, name: str) -> connector_interface.ConnectorResource.State:
        return (
            self.hosts[self.instance]["client"]
            .TestUserConnectorResource(
                request=connector_interface.TestUserConnectorResourceRequest(
                    name=f"{self.namespace}/connector-resources/{name}"
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .state
        )

    @grpc_handler
    def execute_connector(self, name: str, inputs: list) -> list:
        return (
            self.hosts[self.instance]["client"]
            .ExecuteUserConnectorResource(
                request=connector_interface.ExecuteUserConnectorResourceRequest(
                    name=f"{self.namespace}/connector-resources/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .outputs
        )

    @grpc_handler
    def watch_connector(self, name: str) -> connector_interface.ConnectorResource.State:
        return (
            self.hosts[self.instance]["client"]
            .WatchUserConnectorResource(
                request=connector_interface.WatchUserConnectorResourceRequest(
                    name=f"{self.namespace}/connector-resources/{name}"
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .state
        )

    @grpc_handler
    def delete_connector(self, name: str):
        self.hosts[self.instance]["client"].DeleteUserConnectorResource(
            request=connector_interface.DeleteUserConnectorResourceRequest(
                name=f"{self.namespace}/connector-resources/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

    @grpc_handler
    def list_connectors(self, public=False) -> Tuple[list, str, int]:
        if not public:
            resp = self.hosts[self.instance]["client"].ListUserConnectorResources(
                request=connector_interface.ListUserConnectorResourcesRequest(
                    parent=self.namespace
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
        else:
            resp = self.hosts[self.instance]["client"].ListConnectorResources(
                request=connector_interface.ListConnectorResourcesRequest(),
                metadata=(self.hosts[self.instance]["metadata"],),
            )

        return resp.connector_resources, resp.next_page_token, resp.total_size

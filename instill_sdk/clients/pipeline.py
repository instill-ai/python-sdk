# pylint: disable=no-member,wrong-import-position
from typing import Tuple
import grpc

# mgmt
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface

# from instill_sdk.utils.logger import Logger
import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# pipeline
import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_public_service_pb2_grpc as pipeline_service

# common
from instill_sdk.clients.client import Client
from instill_sdk.utils.error_handler import grpc_handler


class PipelineClient(Client):
    def __init__(
        self, user: mgmt_interface.User, protocol="http", host="localhost", port="9080"
    ) -> None:
        """Initialize client for pipeline service with target host.

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
        self._stub = pipeline_service.PipelinePublicServiceStub(self._channel)

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
    def liveness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        return self._stub.Liveness(request=pipeline_interface.LivenessRequest()).status

    @grpc_handler
    def readiness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        return self._stub.Readiness(
            request=pipeline_interface.ReadinessRequest()
        ).status

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
    def create_pipeline(
        self,
        pipeline_name: str,
        recipe: pipeline_interface.Recipe,
    ) -> pipeline_interface.Pipeline:
        pipeline = pipeline_interface.Pipeline(
            id=pipeline_name,
            recipe=recipe,
        )
        resp = self._stub.CreateUserPipeline(
            request=pipeline_interface.CreateUserPipelineRequest(
                pipeline=pipeline, parent=self._user.name
            )
        )
        return resp.pipeline

    @grpc_handler
    def get_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        return self._stub.GetUserPipeline(
            request=pipeline_interface.GetUserPipelineRequest(
                name=f"{self._user.name}/pipelines/{name}"
            )
        ).pipeline

    @grpc_handler
    def validate_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        return self._stub.ValidateUserPipeline(
            request=pipeline_interface.ValidateUserPipelineRequest(
                name=f"{self._user.name}/pipelines/{name}"
            )
        ).pipeline

    @grpc_handler
    def trigger_pipeline(
        self, name: str, inputs: list
    ) -> Tuple[list, pipeline_interface.TriggerMetadata]:
        resp = self._stub.TriggerUserPipeline(
            request=pipeline_interface.TriggerUserPipelineRequest(
                name=f"{self._user.name}/pipelines/{name}", inputs=inputs
            )
        )
        return resp.pipeline, resp.metadata

    @grpc_handler
    def delete_pipeline(self, name: str):
        self._stub.DeleteUserPipeline(
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self._user.name}/pipelines/{name}"
            )
        )

    @grpc_handler
    def list_pipelines(self) -> Tuple[list, str, int]:
        resp = self._stub.ListUserPipelines(
            pipeline_interface.ListUserPipelinesRequest(parent=self._user.name)
        )
        return (resp.pipelines, resp.next_page_token, resp.total_size)

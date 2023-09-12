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
        self, user: mgmt_interface.User, token="", host="localhost", port="8080"
    ) -> None:
        """Initialize client for pipeline service with target host.

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
        self._stub = pipeline_service.PipelinePublicServiceStub(self._channel)

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
    def liveness(self) -> pipeline_interface.LivenessResponse:
        return self._stub.Liveness(request=pipeline_interface.LivenessRequest())

    @grpc_handler
    def readiness(self) -> pipeline_interface.ReadinessResponse:
        return self._stub.Readiness(request=pipeline_interface.ReadinessRequest())

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
        name: str,
        recipe: pipeline_interface.Recipe,
    ) -> pipeline_interface.Pipeline:
        pipeline = pipeline_interface.Pipeline(
            id=name,
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
        return resp.outputs, resp.metadata

    @grpc_handler
    def delete_pipeline(self, name: str):
        self._stub.DeleteUserPipeline(
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self._user.name}/pipelines/{name}"
            )
        )

    @grpc_handler
    def list_pipelines(self) -> list:
        pipelines = []
        resp = self._stub.ListUserPipelines(
            pipeline_interface.ListUserPipelinesRequest(parent=self._user.name)
        )
        pipelines.extend(resp.pipelines)
        while resp.next_page_token != "":
            resp = self._stub.ListUserPipelines(
                pipeline_interface.ListUserPipelinesRequest(
                    parent=self._user.name,
                    page_token=resp.next_page_token,
                )
            )
            pipelines.extend(resp.pipelines)

        return pipelines

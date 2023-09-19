# pylint: disable=no-member,wrong-import-position
from collections import defaultdict
from typing import Tuple

import grpc

import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# pipeline
import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_public_service_pb2_grpc as pipeline_service

# common
from instill_sdk.clients.client import Client
from instill_sdk.configuration import global_config
from instill_sdk.utils.error_handler import grpc_handler

# from instill_sdk.utils.logger import Logger


class PipelineClient(Client):
    def __init__(self, namespace: str) -> None:
        self.hosts = defaultdict(dict)
        self.instance = "default"
        self.namespace = namespace

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
                self.hosts[instance][
                    "client"
                ] = pipeline_service.PipelinePublicServiceStub(channel)

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

    @grpc_handler
    def liveness(self) -> pipeline_interface.LivenessResponse:
        return self.hosts[self.instance]["client"].Liveness(
            request=pipeline_interface.LivenessRequest()
        )

    @grpc_handler
    def readiness(self) -> pipeline_interface.ReadinessResponse:
        return self.hosts[self.instance]["client"].Readiness(
            request=pipeline_interface.ReadinessRequest()
        )

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
        resp = self.hosts[self.instance]["client"].CreateUserPipeline(
            request=pipeline_interface.CreateUserPipelineRequest(
                pipeline=pipeline, parent=self.namespace
            )
        )
        return resp.pipeline

    @grpc_handler
    def get_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        return (
            self.hosts[self.instance]["client"]
            .GetUserPipeline(
                request=pipeline_interface.GetUserPipelineRequest(
                    name=f"{self.namespace}/pipelines/{name}"
                )
            )
            .pipeline
        )

    @grpc_handler
    def validate_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        return (
            self.hosts[self.instance]["client"]
            .ValidateUserPipeline(
                request=pipeline_interface.ValidateUserPipelineRequest(
                    name=f"{self.namespace}/pipelines/{name}"
                )
            )
            .pipeline
        )

    @grpc_handler
    def trigger_pipeline(
        self, name: str, inputs: list
    ) -> Tuple[list, pipeline_interface.TriggerMetadata]:
        resp = self.hosts[self.instance]["client"].TriggerUserPipeline(
            request=pipeline_interface.TriggerUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}", inputs=inputs
            )
        )
        return resp.outputs, resp.metadata

    @grpc_handler
    def delete_pipeline(self, name: str):
        self.hosts[self.instance]["client"].DeleteUserPipeline(
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}"
            )
        )

    @grpc_handler
    def list_pipelines(self) -> list:
        pipelines = []
        resp = self.hosts[self.instance]["client"].ListUserPipelines(
            pipeline_interface.ListUserPipelinesRequest(parent=self.namespace)
        )
        pipelines.extend(resp.pipelines)
        while resp.next_page_token != "":
            resp = self.hosts[self.instance]["client"].ListUserPipelines(
                pipeline_interface.ListUserPipelinesRequest(
                    parent=self.namespace,
                    page_token=resp.next_page_token,
                )
            )
            pipelines.extend(resp.pipelines)

        return pipelines

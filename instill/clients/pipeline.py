# pylint: disable=no-member,wrong-import-position
from collections import defaultdict
from typing import Tuple

import grpc

import instill.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# pipeline
import instill.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
import instill.protogen.vdp.pipeline.v1alpha.pipeline_public_service_pb2_grpc as pipeline_service
from instill.clients import constant

# common
from instill.clients.base import Client
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler

# from instill.utils.logger import Logger


class PipelineClient(Client):
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

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: str):
        self._metadata = metadata

    def liveness(self) -> pipeline_interface.LivenessResponse:
        return self.hosts[self.instance]["client"].Liveness(
            request=pipeline_interface.LivenessRequest()
        )

    def readiness(self) -> pipeline_interface.ReadinessResponse:
        return self.hosts[self.instance]["client"].Readiness(
            request=pipeline_interface.ReadinessRequest()
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
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def get_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        return (
            self.hosts[self.instance]["client"]
            .GetUserPipeline(
                request=pipeline_interface.GetUserPipelineRequest(
                    name=f"{self.namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance]["metadata"],
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
                ),
                metadata=self.hosts[self.instance]["metadata"],
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
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.outputs, resp.metadata

    @grpc_handler
    def delete_pipeline(self, name: str):
        self.hosts[self.instance]["client"].DeleteUserPipeline(
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

    @grpc_handler
    def list_pipelines(self, public=False) -> Tuple[list, str, int]:
        if not public:
            resp = self.hosts[self.instance]["client"].ListUserPipelines(
                request=pipeline_interface.ListUserPipelinesRequest(
                    parent=self.namespace
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
        else:
            resp = self.hosts[self.instance]["client"].ListPipelines(
                request=pipeline_interface.ListPipelinesRequest(),
                metadata=self.hosts[self.instance]["metadata"],
            )

        return resp.pipelines, resp.next_page_token, resp.total_size

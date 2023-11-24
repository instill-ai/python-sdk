# pylint: disable=no-member,wrong-import-position
from collections import defaultdict
from typing import Iterable, Tuple, Union

import grpc
from google.longrunning import operations_pb2
from google.protobuf import field_mask_pb2

import instill.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# pipeline
import instill.protogen.vdp.pipeline.v1alpha.connector_pb2 as connector_interface
import instill.protogen.vdp.pipeline.v1alpha.operator_definition_pb2 as operator_interface
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

    def liveness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        resp: pipeline_interface.LivenessResponse = self.hosts[self.instance][
            "client"
        ].Liveness(request=pipeline_interface.LivenessRequest())
        return resp.health_check_response.status

    def readiness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        resp: pipeline_interface.ReadinessResponse = self.hosts[self.instance][
            "client"
        ].Readiness(request=pipeline_interface.ReadinessRequest())
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
    def list_operator_definitions(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
    ) -> Tuple[Iterable, str, int]:
        resp: operator_interface.ListOperatorDefinitionsResponse = self.hosts[
            self.instance
        ]["client"].ListUserPipelines(
            request=operator_interface.ListOperatorDefinitionsRequest(
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                view=operator_interface.ListOperatorDefinitionsRequest.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

        return resp.operator_definitions, resp.next_page_token, resp.total_size

    @grpc_handler
    def get_operator_definition(
        self, name: str
    ) -> operator_interface.OperatorDefinition:
        resp: operator_interface.GetOperatorDefinitionResponse = self.hosts[
            self.instance
        ]["client"].GetOperatorDefinition(
            request=operator_interface.GetOperatorDefinitionRequest(
                name=f"operator-definitions//{name}",
                view=operator_interface.GetOperatorDefinitionRequest.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.operator_definition

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
        resp: pipeline_interface.CreateUserPipelineResponse = self.hosts[self.instance][
            "client"
        ].CreateUserPipeline(
            request=pipeline_interface.CreateUserPipelineRequest(
                pipeline=pipeline, parent=self.namespace
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def get_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        resp: pipeline_interface.GetUserPipelineResponse = self.hosts[self.instance][
            "client"
        ].GetUserPipeline(
            request=pipeline_interface.GetUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def lookup_pipeline(self, pipeline_uid: str) -> pipeline_interface.Pipeline:
        resp: pipeline_interface.LookUpPipelineResponse = self.hosts[self.instance][
            "client"
        ].LookUpPipeline(
            request=pipeline_interface.LookUpPipelineRequest(
                permalink=f"pipelines/{pipeline_uid}",
                view=pipeline_interface.LookUpPipelineRequest.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def rename_pipeline(self, name: str, new_name: str) -> pipeline_interface.Pipeline:
        resp: pipeline_interface.RenameUserPipelineResponse = self.hosts[self.instance][
            "client"
        ].RenameUserPipeline(
            request=pipeline_interface.RenameUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}",
                new_pipeline_id=new_name,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def update_pipeline(
        self, pipeline: pipeline_interface.Pipeline, mask: field_mask_pb2.FieldMask
    ) -> pipeline_interface.Pipeline:
        resp: pipeline_interface.UpdateUserPipelineResponse = self.hosts[self.instance][
            "client"
        ].UpdateUserPipeline(
            request=pipeline_interface.UpdateUserPipelineRequest(
                pipeline=pipeline,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def validate_pipeline(self, name: str) -> pipeline_interface.Pipeline:
        resp: pipeline_interface.ValidateUserPipelineResponse = self.hosts[
            self.instance
        ]["client"].ValidateUserPipeline(
            request=pipeline_interface.ValidateUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.pipeline

    @grpc_handler
    def trigger_pipeline(
        self, name: str, inputs: list
    ) -> Tuple[Iterable, pipeline_interface.TriggerMetadata]:
        resp: pipeline_interface.TriggerUserPipelineResponse = self.hosts[
            self.instance
        ]["client"].TriggerUserPipeline(
            request=pipeline_interface.TriggerUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.outputs, resp.metadata

    @grpc_handler
    def trigger_async_pipeline(
        self, name: str, inputs: list
    ) -> operations_pb2.Operation:
        resp: pipeline_interface.TriggerAsyncUserPipelineResponse = self.hosts[
            self.instance
        ]["client"].TriggerAsyncUserPipeline(
            request=pipeline_interface.TriggerAsyncUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.operation

    @grpc_handler
    def delete_pipeline(self, name: str):
        self.hosts[self.instance]["client"].DeleteUserPipeline(
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self.namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

    @grpc_handler
    def list_pipelines(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        public=False,
    ) -> Tuple[Iterable, str, int]:
        resp: Union[
            pipeline_interface.ListPipelinesResponse,
            pipeline_interface.ListUserPipelinesResponse,
        ]
        if not public:
            resp = self.hosts[self.instance]["client"].ListUserPipelines(
                request=pipeline_interface.ListUserPipelinesRequest(
                    parent=self.namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.ListUserPipelinesRequest.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
        else:
            resp = self.hosts[self.instance]["client"].ListPipelines(
                request=pipeline_interface.ListPipelinesRequest(
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.ListPipelinesRequest.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )

        return resp.pipelines, resp.next_page_token, resp.total_size

    @grpc_handler
    def get_operation(self, name: str) -> operations_pb2.Operation:
        resp: pipeline_interface.GetOperationResponse = self.hosts[self.instance][
            "client"
        ].GetOperation(
            request=pipeline_interface.GetOperationRequest(
                name=name,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.operation

    @grpc_handler
    def create_pipeline_release(
        self,
        version: str,
    ) -> pipeline_interface.PipelineRelease:
        """Create a release version of a pipeline

        Args:
            name (str): Must be a sematic version vX.Y.Z

        Returns:
            pipeline_interface.PipelineRelease: Released pipeline
        """
        pipeline_release = pipeline_interface.PipelineRelease(
            id=version,
        )
        resp: pipeline_interface.CreateUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].CreateUserPipelineRelease(
            request=pipeline_interface.CreateUserPipelineReleaseRequest(
                release=pipeline_release, parent=self.namespace
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.release

    @grpc_handler
    def get_pipeline_release(self, name: str) -> pipeline_interface.PipelineRelease:
        """Get a released pipeline

        Args:
            name (str): Must have the format of {name}/releases/*

        Returns:
            pipeline_interface.Pipeline: Released pipeline
        """
        resp: pipeline_interface.GetUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].GetUserPipelineRelease(
            request=pipeline_interface.GetUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}",
                view=pipeline_interface.GetUserPipelineReleaseRequest.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.release

    @grpc_handler
    def rename_pipeline_release(
        self, name: str, new_version: str
    ) -> pipeline_interface.PipelineRelease:
        """Rename a released pipeline

        Args:
            name (str): Must have the format of {name}/releases/*
            new_version (str): New release version, must be a sematic version vX.Y.Z

        Returns:
            pipeline_interface.PipelineRelease: released pipeline
        """
        resp: pipeline_interface.RenameUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].RenameUserPipelineRelease(
            request=pipeline_interface.RenameUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}",
                new_pipeline_release_id=new_version,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.release

    @grpc_handler
    def update_pipeline_release(
        self,
        pipeline_release: pipeline_interface.PipelineRelease,
        mask: field_mask_pb2.FieldMask,
    ) -> pipeline_interface.PipelineRelease:
        resp: pipeline_interface.UpdateUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].UpdateUserPipelineRelease(
            request=pipeline_interface.UpdateUserPipelineReleaseRequest(
                release=pipeline_release,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.release

    @grpc_handler
    def list_pipeline_releases(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
    ) -> Tuple[Iterable, str, int]:
        resp: pipeline_interface.ListUserPipelineReleasesResponse = self.hosts[
            self.instance
        ]["client"].ListUserPipelineReleases(
            request=pipeline_interface.ListUserPipelineReleasesRequest(
                parent=self.namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.ListUserPipelineReleasesRequest.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

        return resp.releases, resp.next_page_token, resp.total_size

    @grpc_handler
    def delete_pipeline_release(self, name: str):
        self.hosts[self.instance]["client"].DeleteUserPipelineRelease(
            request=pipeline_interface.DeleteUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

    @grpc_handler
    def set_default_pipeline_release(
        self, name: str
    ) -> pipeline_interface.PipelineRelease:
        resp: pipeline_interface.SetDefaultUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].SetDefaultUserPipelineRelease(
            request=pipeline_interface.SetDefaultUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.release

    @grpc_handler
    def restore_pipeline_release(self, name: str) -> pipeline_interface.PipelineRelease:
        resp: pipeline_interface.RestoreUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].RestoreUserPipelineRelease(
            request=pipeline_interface.RestoreUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.release

    @grpc_handler
    def watch_pipeline_release(self, name: str) -> pipeline_interface.State.ValueType:
        resp: pipeline_interface.WatchUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].WatchUserPipelineRelease(
            request=pipeline_interface.WatchUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.state

    @grpc_handler
    def trigger_pipeline_release(
        self, name: str, inputs: list
    ) -> Tuple[Iterable, pipeline_interface.TriggerMetadata]:
        resp: pipeline_interface.TriggerUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].TriggerUserPipelineReleas(
            request=pipeline_interface.TriggerUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.outputs, resp.metadata

    @grpc_handler
    def trigger_async_pipeline_release(
        self, name: str, inputs: list
    ) -> operations_pb2.Operation:
        resp: pipeline_interface.TriggerAsyncUserPipelineReleaseResponse = self.hosts[
            self.instance
        ]["client"].TriggerAsyncUserPipelineRelease(
            request=pipeline_interface.TriggerAsyncUserPipelineReleaseRequest(
                name=f"{self.namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )
        return resp.operation

    @grpc_handler
    def create_connector(
        self,
        name: str,
        definition: str,
        configuration: dict,
    ) -> connector_interface.Connector:
        connector = connector_interface.Connector()
        connector.id = name
        connector.connector_definition_name = definition
        connector.configuration.update(configuration)
        resp = self.hosts[self.instance]["client"].CreateUserConnector(
            request=connector_interface.CreateUserConnectorRequest(
                connector=connector, parent=self.namespace
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

        return resp.connector

    @grpc_handler
    def get_connector(self, name: str) -> connector_interface.Connector:
        return (
            self.hosts[self.instance]["client"]
            .GetUserConnector(
                request=connector_interface.GetUserConnectorRequest(
                    name=f"{self.namespace}/connectors/{name}",
                    view=connector_interface.GetUserConnectorRequest.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .connector
        )

    @grpc_handler
    def test_connector(self, name: str) -> connector_interface.Connector.State:
        return (
            self.hosts[self.instance]["client"]
            .TestUserConnector(
                request=connector_interface.TestUserConnectorRequest(
                    name=f"{self.namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .state
        )

    @grpc_handler
    def execute_connector(self, name: str, inputs: list) -> list:
        return (
            self.hosts[self.instance]["client"]
            .ExecuteUserConnector(
                request=connector_interface.ExecuteUserConnectorRequest(
                    name=f"{self.namespace}/connectors/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .outputs
        )

    @grpc_handler
    def watch_connector(self, name: str) -> connector_interface.Connector.State:
        return (
            self.hosts[self.instance]["client"]
            .WatchUserConnector(
                request=connector_interface.WatchUserConnectorRequest(
                    name=f"{self.namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
            .state
        )

    @grpc_handler
    def delete_connector(self, name: str):
        self.hosts[self.instance]["client"].DeleteUserConnector(
            request=connector_interface.DeleteUserConnectorRequest(
                name=f"{self.namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance]["metadata"],
        )

    @grpc_handler
    def list_connectors(self, public=False) -> Tuple[list, str, int]:
        if not public:
            resp = self.hosts[self.instance]["client"].ListUserConnectors(
                request=connector_interface.ListUserConnectorsRequest(
                    parent=self.namespace
                ),
                metadata=self.hosts[self.instance]["metadata"],
            )
        else:
            resp = self.hosts[self.instance]["client"].ListConnectors(
                request=connector_interface.ListConnectorsRequest(),
                metadata=(self.hosts[self.instance]["metadata"],),
            )

        return resp.connectors, resp.next_page_token, resp.total_size

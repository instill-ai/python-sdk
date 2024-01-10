# pylint: disable=no-member,wrong-import-position,too-many-lines
from typing import Dict, Union

from google.protobuf import field_mask_pb2

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck

# pipeline
import instill.protogen.vdp.pipeline.v1beta.connector_pb2 as connector_interface
import instill.protogen.vdp.pipeline.v1beta.operator_definition_pb2 as operator_interface
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
import instill.protogen.vdp.pipeline.v1beta.pipeline_public_service_pb2_grpc as pipeline_service
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler

# from instill.utils.logger import Logger


class PipelineClient(Client):
    def __init__(
        self, namespace: str, async_enabled: bool, target_namespace: str = ""
    ) -> None:
        self.hosts: Dict[str, InstillInstance] = {}
        self.namespace: str = namespace
        self.target_namespace: str = (
            namespace if target_namespace == "" else target_namespace
        )
        if DEFAULT_INSTANCE in global_config.hosts:
            self.instance = DEFAULT_INSTANCE
        elif len(global_config.hosts) == 0:
            self.instance = ""
        else:
            self.instance = list(global_config.hosts.keys())[0]

        if global_config.hosts is not None:
            for instance, config in global_config.hosts.items():
                self.hosts[instance] = InstillInstance(
                    pipeline_service.PipelinePublicServiceStub,
                    url=config.url,
                    token=config.token,
                    secure=config.secure,
                    async_enabled=async_enabled,
                )

    @property
    def hosts(self):
        return self._hosts

    @hosts.setter
    def hosts(self, hosts: Dict[str, InstillInstance]):
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

    def liveness(
        self, async_enabled: bool = False
    ) -> pipeline_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Liveness,
                request=pipeline_interface.LivenessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Liveness,
            request=pipeline_interface.LivenessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    def readiness(
        self, async_enabled: bool = False
    ) -> pipeline_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Readiness,
                request=pipeline_interface.ReadinessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Readiness,
            request=pipeline_interface.ReadinessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    def is_serving(self) -> bool:
        try:
            return (
                self.readiness().health_check_response.status
                == healthcheck.HealthCheckResponse.SERVING_STATUS_SERVING
            )
        except Exception:
            return False

    @grpc_handler
    def list_operator_definitions(
        self,
        filter_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        async_enabled: bool = False,
    ) -> operator_interface.ListOperatorDefinitionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOperatorDefinitions,
                request=operator_interface.ListOperatorDefinitionsRequest(
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    view=operator_interface.OperatorDefinition.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListOperatorDefinitions,
            request=operator_interface.ListOperatorDefinitionsRequest(
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                view=operator_interface.OperatorDefinition.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_operator_definition(
        self, name: str, async_enabled: bool = False
    ) -> operator_interface.GetOperatorDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOperatorDefinition,
                request=operator_interface.GetOperatorDefinitionRequest(
                    name=f"operator-definitions/{name}",
                    view=operator_interface.OperatorDefinition.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOperatorDefinition,
            request=operator_interface.GetOperatorDefinitionRequest(
                name=f"operator-definitions/{name}",
                view=operator_interface.OperatorDefinition.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_pipeline(
        self,
        name: str,
        recipe: pipeline_interface.Recipe,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateUserPipelineResponse:
        pipeline = pipeline_interface.Pipeline(
            id=name,
            recipe=recipe,
        )
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateUserPipeline,
                request=pipeline_interface.CreateUserPipelineRequest(
                    pipeline=pipeline, parent=self.target_namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateUserPipeline,
            request=pipeline_interface.CreateUserPipelineRequest(
                pipeline=pipeline, parent=self.target_namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserPipeline,
                request=pipeline_interface.GetUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserPipeline,
            request=pipeline_interface.GetUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def lookup_pipeline(
        self,
        pipeline_uid: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.LookUpPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.LookUpPipeline,
                request=pipeline_interface.LookUpPipelineRequest(
                    permalink=f"pipelines/{pipeline_uid}",
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.LookUpPipeline,
            request=pipeline_interface.LookUpPipelineRequest(
                permalink=f"pipelines/{pipeline_uid}",
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def rename_pipeline(
        self,
        name: str,
        new_name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RenameUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.RenameUserPipeline,
                request=pipeline_interface.RenameUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    new_pipeline_id=new_name,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RenameUserPipeline,
            request=pipeline_interface.RenameUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                new_pipeline_id=new_name,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_pipeline(
        self,
        pipeline: pipeline_interface.Pipeline,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateUserPipeline,
                request=pipeline_interface.UpdateUserPipelineRequest(
                    pipeline=pipeline,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserPipeline,
            request=pipeline_interface.UpdateUserPipelineRequest(
                pipeline=pipeline,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def validate_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.ValidateUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ValidateUserPipeline,
                request=pipeline_interface.ValidateUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ValidateUserPipeline,
            request=pipeline_interface.ValidateUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_pipeline(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerUserPipeline,
                request=pipeline_interface.TriggerUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserPipeline,
            request=pipeline_interface.TriggerUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_pipeline(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerAsyncUserPipeline,
                request=pipeline_interface.TriggerAsyncUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncUserPipeline,
            request=pipeline_interface.TriggerAsyncUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserPipeline,
                request=pipeline_interface.DeleteUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserPipeline,
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipelines(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        public=False,
        async_enabled: bool = False,
    ) -> Union[
        pipeline_interface.ListPipelinesResponse,
        pipeline_interface.ListUserPipelinesResponse,
    ]:
        if async_enabled:
            if public:
                method = self.hosts[self.instance].async_client.ListPipelines
                return RequestFactory(
                    method=method,
                    request=pipeline_interface.ListPipelinesRequest(
                        filter=filer_str,
                        page_size=total_size,
                        page_token=next_page_token,
                        show_deleted=show_deleted,
                        view=pipeline_interface.Pipeline.VIEW_FULL,
                    ),
                    metadata=self.hosts[self.instance].metadata,
                ).send_async()
            method = self.hosts[self.instance].async_client.ListUserPipelines
            return RequestFactory(
                method=method,
                request=pipeline_interface.ListUserPipelinesRequest(
                    parent=self.target_namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        if public:
            method = self.hosts[self.instance].client.ListPipelines
            return RequestFactory(
                method=method,
                request=pipeline_interface.ListPipelinesRequest(
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_sync()
        method = self.hosts[self.instance].client.ListUserPipelines
        return RequestFactory(
            method=method,
            request=pipeline_interface.ListUserPipelinesRequest(
                parent=self.target_namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_operation(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOperation,
                request=pipeline_interface.GetOperationRequest(
                    name=name,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOperation,
            request=pipeline_interface.GetOperationRequest(
                name=name,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_pipeline_release(
        self,
        version: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateUserPipelineReleaseResponse:
        """Create a release version of a pipeline

        Args:
            name (str): Must be a sematic version vX.Y.Z

        Returns:
            pipeline_interface.PipelineRelease: Released pipeline
        """
        pipeline_release = pipeline_interface.PipelineRelease(
            id=version,
        )
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateUserPipelineRelease,
                request=pipeline_interface.CreateUserPipelineReleaseRequest(
                    release=pipeline_release, parent=self.target_namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateUserPipelineRelease,
            request=pipeline_interface.CreateUserPipelineReleaseRequest(
                release=pipeline_release, parent=self.target_namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetUserPipelineReleaseResponse:
        """Get a released pipeline

        Args:
            name (str): Must have the format of {name}/releases/*

        Returns:
            pipeline_interface.Pipeline: Released pipeline
        """
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserPipelineRelease,
                request=pipeline_interface.GetUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserPipelineRelease,
            request=pipeline_interface.GetUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def rename_pipeline_release(
        self,
        name: str,
        new_version: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RenameUserPipelineReleaseResponse:
        """Rename a released pipeline

        Args:
            name (str): Must have the format of {name}/releases/*
            new_version (str): New release version, must be a sematic version vX.Y.Z

        Returns:
            pipeline_interface.PipelineRelease: released pipeline
        """
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.RenameUserPipelineRelease,
                request=pipeline_interface.RenameUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    new_pipeline_release_id=new_version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RenameUserPipelineRelease,
            request=pipeline_interface.RenameUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                new_pipeline_release_id=new_version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_pipeline_release(
        self,
        pipeline_release: pipeline_interface.PipelineRelease,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateUserPipelineRelease,
                request=pipeline_interface.UpdateUserPipelineReleaseRequest(
                    release=pipeline_release,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserPipelineRelease,
            request=pipeline_interface.UpdateUserPipelineReleaseRequest(
                release=pipeline_release,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_releases(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListUserPipelineReleasesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListUserPipelineReleases,
                request=pipeline_interface.ListUserPipelineReleasesRequest(
                    parent=self.target_namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListUserPipelineReleases,
            request=pipeline_interface.ListUserPipelineReleasesRequest(
                parent=self.target_namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserPipelineRelease,
                request=pipeline_interface.DeleteUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserPipelineRelease,
            request=pipeline_interface.DeleteUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def restore_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RestoreUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.RestoreUserPipelineRelease,
                request=pipeline_interface.RestoreUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RestoreUserPipelineRelease,
            request=pipeline_interface.RestoreUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.WatchUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.WatchUserPipelineRelease,
                request=pipeline_interface.WatchUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchUserPipelineRelease,
            request=pipeline_interface.WatchUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_pipeline_release(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerUserPipelineRelease,
                request=pipeline_interface.TriggerUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserPipelineRelease,
            request=pipeline_interface.TriggerUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_pipeline_release(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncUserPipelineRelease,
                request=pipeline_interface.TriggerAsyncUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncUserPipelineRelease,
            request=pipeline_interface.TriggerAsyncUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_org_pipeline(
        self,
        name: str,
        recipe: pipeline_interface.Recipe,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateOrganizationPipelineResponse:
        pipeline = pipeline_interface.Pipeline(
            id=name,
            recipe=recipe,
        )
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.CreateOrganizationPipeline,
                request=pipeline_interface.CreateOrganizationPipelineRequest(
                    pipeline=pipeline, parent=self.target_namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateOrganizationPipeline,
            request=pipeline_interface.CreateOrganizationPipelineRequest(
                pipeline=pipeline, parent=self.target_namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_org_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserPipeline,
                request=pipeline_interface.GetUserPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserPipeline,
            request=pipeline_interface.GetUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def rename_org_pipeline(
        self,
        name: str,
        new_name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RenameOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.RenameOrganizationPipeline,
                request=pipeline_interface.RenameOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    new_pipeline_id=new_name,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RenameOrganizationPipeline,
            request=pipeline_interface.RenameOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                new_pipeline_id=new_name,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_org_pipeline(
        self,
        pipeline: pipeline_interface.Pipeline,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateOrganizationPipeline,
                request=pipeline_interface.UpdateOrganizationPipelineRequest(
                    pipeline=pipeline,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationPipeline,
            request=pipeline_interface.UpdateOrganizationPipelineRequest(
                pipeline=pipeline,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def validate_org_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.ValidateUserPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ValidateOrganizationPipeline,
                request=pipeline_interface.ValidateOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ValidateOrganizationPipeline,
            request=pipeline_interface.ValidateOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_org_pipeline(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationPipeline,
                request=pipeline_interface.TriggerOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationPipeline,
            request=pipeline_interface.TriggerOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_org_async_pipeline(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncOrganizationPipeline,
                request=pipeline_interface.TriggerAsyncOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncOrganizationPipeline,
            request=pipeline_interface.TriggerAsyncOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_org_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.DeleteOrganizationPipeline,
                request=pipeline_interface.DeleteOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationPipeline,
            request=pipeline_interface.DeleteOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_org_pipelines(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListOrganizationPipelinesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOrganizationPipelines,
                request=pipeline_interface.ListOrganizationPipelinesRequest(
                    parent=self.target_namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationPipelines,
            request=pipeline_interface.ListOrganizationPipelinesRequest(
                parent=self.target_namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_org_pipeline_release(
        self,
        version: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateOrganizationPipelineReleaseResponse:
        """Create a release version of a pipeline

        Args:
            name (str): Must be a sematic version vX.Y.Z

        Returns:
            pipeline_interface.PipelineRelease: Released pipeline
        """
        pipeline_release = pipeline_interface.PipelineRelease(
            id=version,
        )
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.CreateOrganizationPipelineRelease,
                request=pipeline_interface.CreateOrganizationPipelineReleaseRequest(
                    release=pipeline_release, parent=self.target_namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateOrganizationPipelineRelease,
            request=pipeline_interface.CreateOrganizationPipelineReleaseRequest(
                release=pipeline_release, parent=self.target_namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_org_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetOrganizationPipelineReleaseResponse:
        """Get a released pipeline

        Args:
            name (str): Must have the format of {name}/releases/*

        Returns:
            pipeline_interface.Pipeline: Released pipeline
        """
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.GetOrganizationPipelineRelease,
                request=pipeline_interface.GetOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationPipelineRelease,
            request=pipeline_interface.GetOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def rename_org_pipeline_release(
        self,
        name: str,
        new_version: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RenameOrganizationPipelineReleaseResponse:
        """Rename a released pipeline

        Args:
            name (str): Must have the format of {name}/releases/*
            new_version (str): New release version, must be a sematic version vX.Y.Z

        Returns:
            pipeline_interface.PipelineRelease: released pipeline
        """
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.RenameOrganizationPipelineRelease,
                request=pipeline_interface.RenameOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    new_pipeline_release_id=new_version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RenameOrganizationPipelineRelease,
            request=pipeline_interface.RenameOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                new_pipeline_release_id=new_version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_org_pipeline_release(
        self,
        pipeline_release: pipeline_interface.PipelineRelease,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateOrganizationPipelineRelease,
                request=pipeline_interface.UpdateOrganizationPipelineReleaseRequest(
                    release=pipeline_release,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationPipelineRelease,
            request=pipeline_interface.UpdateOrganizationPipelineReleaseRequest(
                release=pipeline_release,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_org_pipeline_releases(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListOrganizationPipelineReleasesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListOrganizationPipelineReleases,
                request=pipeline_interface.ListOrganizationPipelineReleasesRequest(
                    parent=self.target_namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationPipelineReleases,
            request=pipeline_interface.ListOrganizationPipelineReleasesRequest(
                parent=self.target_namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_org_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.DeleteOrganizationPipelineRelease,
                request=pipeline_interface.DeleteOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationPipelineRelease,
            request=pipeline_interface.DeleteOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def restore_org_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RestoreOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.RestoreOrganizationPipelineRelease,
                request=pipeline_interface.RestoreOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RestoreOrganizationPipelineRelease,
            request=pipeline_interface.RestoreOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_org_pipeline_release(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.WatchOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.WatchOrganizationPipelineRelease,
                request=pipeline_interface.WatchOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchOrganizationPipelineRelease,
            request=pipeline_interface.WatchOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_org_pipeline_release(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationPipelineRelease,
                request=pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationPipelineRelease,
            request=pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_org_pipeline_release(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncOrganizationPipelineRelease,
                request=pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[
                self.instance
            ].client.TriggerAsyncOrganizationPipelineRelease,
            request=pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_connector(
        self,
        name: str,
        definition: str,
        configuration: dict,
        async_enabled: bool = False,
    ) -> connector_interface.CreateUserConnectorResponse:
        connector = connector_interface.Connector()
        connector.id = name
        connector.connector_definition_name = definition
        connector.configuration.update(configuration)
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateUserConnector,
                request=connector_interface.CreateUserConnectorRequest(
                    connector=connector, parent=self.target_namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateUserConnector,
            request=connector_interface.CreateUserConnectorRequest(
                connector=connector, parent=self.target_namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.GetUserConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserConnector,
                request=connector_interface.GetUserConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}",
                    view=connector_interface.Connector.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserConnector,
            request=connector_interface.GetUserConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}",
                view=connector_interface.Connector.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def test_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.TestUserConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TestUserConnector,
                request=connector_interface.TestUserConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TestUserConnector,
            request=connector_interface.TestUserConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def execute_connector(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> connector_interface.ExecuteUserConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ExecuteUserConnector,
                request=connector_interface.ExecuteUserConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ExecuteUserConnector,
            request=connector_interface.ExecuteUserConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.WatchUserConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.WatchUserConnector,
                request=connector_interface.WatchUserConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchUserConnector,
            request=connector_interface.WatchUserConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.DeleteUserConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserConnector,
                request=connector_interface.DeleteUserConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserConnector,
            request=connector_interface.DeleteUserConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_connectors(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        public=False,
        async_enabled: bool = False,
    ) -> connector_interface.ListUserConnectorsResponse:
        if async_enabled:
            if public:
                method = self.hosts[self.instance].async_client.ListConnectors
                return RequestFactory(
                    method=method,
                    request=connector_interface.ListConnectorsRequest(
                        filter=filer_str,
                        page_size=total_size,
                        page_token=next_page_token,
                        show_deleted=show_deleted,
                        view=connector_interface.Connector.VIEW_FULL,
                    ),
                    metadata=self.hosts[self.instance].metadata,
                ).send_async()
            method = self.hosts[self.instance].async_client.ListUserConnectors
            return RequestFactory(
                method=method,
                request=connector_interface.ListUserConnectorsRequest(
                    parent=self.target_namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=connector_interface.Connector.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        if public:
            method = self.hosts[self.instance].client.ListConnectors
            return RequestFactory(
                method=method,
                request=connector_interface.ListConnectorsRequest(
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=connector_interface.Connector.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_sync()
        method = self.hosts[self.instance].client.ListUserConnectors
        return RequestFactory(
            method=method,
            request=connector_interface.ListUserConnectorsRequest(
                parent=self.target_namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=connector_interface.Connector.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_org_connector(
        self,
        name: str,
        definition: str,
        configuration: dict,
        async_enabled: bool = False,
    ) -> connector_interface.CreateOrganizationConnectorResponse:
        connector = connector_interface.Connector()
        connector.id = name
        connector.connector_definition_name = definition
        connector.configuration.update(configuration)
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.CreateOrganizationConnector,
                request=connector_interface.CreateOrganizationConnectorRequest(
                    connector=connector, parent=self.target_namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateOrganizationConnector,
            request=connector_interface.CreateOrganizationConnectorRequest(
                connector=connector, parent=self.target_namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_org_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.GetOrganizationConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganizationConnector,
                request=connector_interface.GetOrganizationConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}",
                    view=connector_interface.Connector.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationConnector,
            request=connector_interface.GetOrganizationConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}",
                view=connector_interface.Connector.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def test_org_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.TestOrganizationConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TestOrganizationConnector,
                request=connector_interface.TestOrganizationConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TestOrganizationConnector,
            request=connector_interface.TestOrganizationConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def execute_org_connector(
        self,
        name: str,
        inputs: list,
        async_enabled: bool = False,
    ) -> connector_interface.ExecuteOrganizationConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ExecuteOrganizationConnector,
                request=connector_interface.ExecuteOrganizationConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}", inputs=inputs
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ExecuteOrganizationConnector,
            request=connector_interface.ExecuteOrganizationConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}", inputs=inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_org_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.WatchOrganizationConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.WatchOrganizationConnector,
                request=connector_interface.WatchOrganizationConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchOrganizationConnector,
            request=connector_interface.WatchOrganizationConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_org_connector(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> connector_interface.DeleteOrganizationConnectorResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.DeleteOrganizationConnector,
                request=connector_interface.DeleteOrganizationConnectorRequest(
                    name=f"{self.target_namespace}/connectors/{name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationConnector,
            request=connector_interface.DeleteOrganizationConnectorRequest(
                name=f"{self.target_namespace}/connectors/{name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_org_connectors(
        self,
        filer_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> connector_interface.ListOrganizationConnectorsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListOrganizationConnectors,
                request=connector_interface.ListOrganizationConnectorsRequest(
                    parent=self.target_namespace,
                    filter=filer_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=connector_interface.Connector.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationConnectors,
            request=connector_interface.ListOrganizationConnectorsRequest(
                parent=self.target_namespace,
                filter=filer_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=connector_interface.Connector.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

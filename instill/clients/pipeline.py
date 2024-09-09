# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from typing import Dict, Optional, Union

from google.protobuf.struct_pb2 import Struct

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
import instill.protogen.vdp.pipeline.v1beta.component_definition_pb2 as component_definition
import instill.protogen.vdp.pipeline.v1beta.integration_pb2 as integration_interface

# pipeline
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
import instill.protogen.vdp.pipeline.v1beta.pipeline_public_service_pb2_grpc as pipeline_service
import instill.protogen.vdp.pipeline.v1beta.secret_pb2 as secret_interface
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.protogen.vdp.pipeline.v1beta import common_pb2
from instill.utils.error_handler import grpc_handler


class PipelineClient(Client):
    def __init__(
        self,
        namespace: str,
        async_enabled: bool = False,
        target_namespace: str = "",
        api_token: str = "",
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
                token = config.token
                if api_token != "" and instance == self.instance:
                    token = api_token
                self.hosts[instance] = InstillInstance(
                    pipeline_service.PipelinePublicServiceStub,
                    url=config.url,
                    token=token,
                    secure=config.secure,
                    async_enabled=async_enabled,
                )

    def close(self):
        if self.is_serving():
            for host in self.hosts.values():
                host.channel.close()

    async def async_close(self):
        if self.is_serving():
            for host in self.hosts.values():
                await host.async_channel.close()

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

    def set_instance(self, instance: str):
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
    def create_pipeline(
        self,
        name: str,
        description: str,
        recipe: dict,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateUserPipelineResponse:
        pipeline = pipeline_interface.Pipeline(
            id=name,
            description=description,
        )
        pipeline.recipe.update(recipe)
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
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserPipeline,
            request=pipeline_interface.GetUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.LookUpPipeline,
            request=pipeline_interface.LookUpPipelineRequest(
                permalink=f"pipelines/{pipeline_uid}",
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
        pipeline_id: str,
        pipeline_description: str,
        pipeline_documentation_url: str,
        pipeline_license: str,
        pipeline_profile_image: str,
        pipeline_sharing_enabled: bool = False,
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateUserPipelineResponse:
        tags = tags if tags is not None else []
        sharing = common_pb2.Sharing()
        sharing.User.enabled = pipeline_sharing_enabled
        sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        pipeline = pipeline_interface.Pipeline(
            id=pipeline_id,
            description=pipeline_description,
            documentation_url=pipeline_documentation_url,
            license=pipeline_license,
            profile_image=pipeline_profile_image,
            sharing=sharing,
            tags=tags,
        )

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateUserPipeline,
                request=pipeline_interface.UpdateUserPipelineRequest(
                    pipeline=pipeline,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserPipeline,
            request=pipeline_interface.UpdateUserPipelineRequest(
                pipeline=pipeline,
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
    def clone_pipeline(
        self,
        name: str,
        target: str,
        description: str,
        sharing_enabled: bool = False,
        sharing_role_executor: bool = True,
        async_enabled: bool = False,
    ) -> pipeline_interface.CloneUserPipelineResponse:
        sharing = common_pb2.Sharing()
        sharing.User.enabled = sharing_enabled
        if sharing_role_executor:
            sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CloneUserPipeline,
                request=pipeline_interface.CloneUserPipelineRequest(
                    name=f"users/{self.target_namespace}/pipelines/{name}",
                    target=f"{self.target_namespace}/{target}",
                    description=description,
                    sharing=sharing,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CloneUserPipeline,
            request=pipeline_interface.CloneUserPipelineRequest(
                name=f"users/{self.target_namespace}/pipelines/{name}",
                target=f"{self.target_namespace}/{target}",
                description=description,
                sharing=sharing,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_pipeline(
        self,
        name: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerUserPipelineResponse:
        request = pipeline_interface.TriggerUserPipelineRequest(
            name=f"{self.target_namespace}/pipelines/{name}",
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerUserPipeline,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserPipeline,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_pipeline(
        self,
        name: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncUserPipelineResponse:
        request = pipeline_interface.TriggerAsyncUserPipelineRequest(
            name=f"{self.target_namespace}/pipelines/{name}",
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerAsyncUserPipeline,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncUserPipeline,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def send_namespace_pipeline_event(
        self,
        namespace_id: str,
        pipeline_id: str,
        event: str,
        code: str,
        data: dict,
        async_enabled: bool = False,
    ) -> pipeline_interface.SendNamespacePipelineEventResponse:
        trigger_data = Struct()
        trigger_data.update(data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.SendNamespacePipelineEvent,
                request=pipeline_interface.SendNamespacePipelineEventRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    event=event,
                    code=code,
                    data=trigger_data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.SendNamespacePipelineEvent,
            request=pipeline_interface.SendNamespacePipelineEventRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                event=event,
                code=code,
                data=trigger_data,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def send_namespace_pipeline_release_event(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        event: str,
        code: str,
        data: Struct,
        async_enabled: bool = False,
    ) -> pipeline_interface.SendNamespacePipelineReleaseEventResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.SendNamespacePipelineReleaseEvent,
                request=pipeline_interface.SendNamespacePipelineReleaseEventRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    event=event,
                    code=code,
                    data=data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.SendNamespacePipelineReleaseEvent,
            request=pipeline_interface.SendNamespacePipelineReleaseEventRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                event=event,
                code=code,
                data=data,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_namespace_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerNamespacePipelineResponse:
        request = pipeline_interface.TriggerNamespacePipelineRequest(
            namespace_id=namespace_id,
            pipeline_id=pipeline_id,
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerNamespacePipeline,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerNamespacePipeline,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_namespace_pipeline_with_stream(
        self,
        namespace_id: str,
        pipeline_id: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerNamespacePipelineWithStreamResponse:
        request = pipeline_interface.TriggerNamespacePipelineWithStreamRequest(
            namespace_id=namespace_id,
            pipeline_id=pipeline_id,
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerNamespacePipelineWithStream,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerNamespacePipelineWithStream,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_namespace_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncNamespacePipelineResponse:
        request = pipeline_interface.TriggerAsyncNamespacePipelineRequest(
            namespace_id=namespace_id,
            pipeline_id=pipeline_id,
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncNamespacePipeline,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncNamespacePipeline,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release: pipeline_interface.PipelineRelease,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateNamespacePipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.CreateNamespacePipelineRelease,
                request=pipeline_interface.CreateNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release=release,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateNamespacePipelineRelease,
            request=pipeline_interface.CreateNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release=release,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_namespace_pipeline_releases(
        self,
        namespace_id: str,
        pipeline_id: str,
        total_size: int = 10,
        next_page_token: str = "",
        filter_str: str = "",
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListNamespacePipelineReleasesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListNamespacePipelineReleases,
                request=pipeline_interface.ListNamespacePipelineReleasesRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                    show_deleted=show_deleted,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListNamespacePipelineReleases,
            request=pipeline_interface.ListNamespacePipelineReleasesRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
                show_deleted=show_deleted,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetNamespacePipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.GetNamespacePipelineRelease,
                request=pipeline_interface.GetNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetNamespacePipelineRelease,
            request=pipeline_interface.GetNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        release: pipeline_interface.PipelineRelease,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateNamespacePipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateNamespacePipelineRelease,
                request=pipeline_interface.UpdateNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    release=release,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateNamespacePipelineRelease,
            request=pipeline_interface.UpdateNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                release=release,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteNamespacePipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.DeleteNamespacePipelineRelease,
                request=pipeline_interface.DeleteNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteNamespacePipelineRelease,
            request=pipeline_interface.DeleteNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def clone_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        target: str,
        description: str,
        sharing_enabled: bool = False,
        sharing_role_executor: bool = True,
        async_enabled: bool = False,
    ) -> pipeline_interface.CloneNamespacePipelineReleaseResponse:
        sharing = common_pb2.Sharing()
        sharing.User.enabled = sharing_enabled
        if sharing_role_executor:
            sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.CloneNamespacePipelineRelease,
                request=pipeline_interface.CloneNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    target=f"{self.target_namespace}/pipelines/{target}",
                    description=description,
                    sharing=sharing,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CloneNamespacePipelineRelease,
            request=pipeline_interface.CloneNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                target=f"{self.target_namespace}/pipelines/{target}",
                description=description,
                sharing=sharing,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerNamespacePipelineReleaseResponse:
        request = pipeline_interface.TriggerNamespacePipelineReleaseRequest(
            namespace_id=namespace_id,
            pipeline_id=pipeline_id,
            release_id=release_id,
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerNamespacePipelineRelease,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerNamespacePipelineRelease,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_namespace_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncNamespacePipelineReleaseResponse:
        request = pipeline_interface.TriggerAsyncNamespacePipelineReleaseRequest(
            namespace_id=namespace_id,
            pipeline_id=pipeline_id,
            release_id=release_id,
        )
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncNamespacePipelineRelease,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[
                self.instance
            ].client.TriggerAsyncNamespacePipelineRelease,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_namespace_secret(
        self,
        namespace_id: str,
        secret: secret_interface.Secret,
        async_enabled: bool = False,
    ) -> secret_interface.CreateNamespaceSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateNamespaceSecret,
                request=secret_interface.CreateNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret=secret,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateNamespaceSecret,
            request=secret_interface.CreateNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret=secret,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_namespace_secrets(
        self,
        namespace_id: str,
        total_size: int = 10,
        next_page_token: str = "",
        async_enabled: bool = False,
    ) -> secret_interface.ListNamespaceSecretsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListNamespaceSecrets,
                request=secret_interface.ListNamespaceSecretsRequest(
                    namespace_id=namespace_id,
                    page_size=total_size,
                    page_token=next_page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListNamespaceSecrets,
            request=secret_interface.ListNamespaceSecretsRequest(
                namespace_id=namespace_id,
                page_size=total_size,
                page_token=next_page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_namespace_secret(
        self,
        namespace_id: str,
        secret_id: str,
        async_enabled: bool = False,
    ) -> secret_interface.GetNamespaceSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetNamespaceSecret,
                request=secret_interface.GetNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret_id=secret_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetNamespaceSecret,
            request=secret_interface.GetNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret_id=secret_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_namespace_secret(
        self,
        namespace_id: str,
        secret_id: str,
        secret: secret_interface.Secret,
        async_enabled: bool = False,
    ) -> secret_interface.UpdateNamespaceSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateNamespaceSecret,
                request=secret_interface.UpdateNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret_id=secret_id,
                    secret=secret,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateNamespaceSecret,
            request=secret_interface.UpdateNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret_id=secret_id,
                secret=secret,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_namespace_secret(
        self,
        namespace_id: str,
        secret_id: str,
        async_enabled: bool = False,
    ) -> secret_interface.DeleteNamespaceSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteNamespaceSecret,
                request=secret_interface.DeleteNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret_id=secret_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteNamespaceSecret,
            request=secret_interface.DeleteNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret_id=secret_id,
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
                    name=f"{self.target_namespace}/pipelines/{name}/releases/latest"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserPipeline,
            request=pipeline_interface.DeleteUserPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}/releases/latest"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipelines(
        self,
        visibility: pipeline_interface.Pipeline.Visibility.ValueType,
        order_by: str,
        filter_str: str = "",
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
                        filter=filter_str,
                        page_size=total_size,
                        page_token=next_page_token,
                        show_deleted=show_deleted,
                        view=pipeline_interface.Pipeline.VIEW_RECIPE,
                        visibility=visibility,
                        order_by=order_by,
                    ),
                    metadata=self.hosts[self.instance].metadata,
                ).send_async()
            method = self.hosts[self.instance].async_client.ListUserPipelines
            return RequestFactory(
                method=method,
                request=pipeline_interface.ListUserPipelinesRequest(
                    parent=self.target_namespace,
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        if public:
            method = self.hosts[self.instance].client.ListPipelines
            return RequestFactory(
                method=method,
                request=pipeline_interface.ListPipelinesRequest(
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_sync()
        method = self.hosts[self.instance].client.ListUserPipelines
        return RequestFactory(
            method=method,
            request=pipeline_interface.ListUserPipelinesRequest(
                parent=self.target_namespace,
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                visibility=visibility,
                order_by=order_by,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_operation(
        self,
        operation_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOperation,
                request=pipeline_interface.GetOperationRequest(
                    operation_id=operation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOperation,
            request=pipeline_interface.GetOperationRequest(
                operation_id=operation_id,
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
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserPipelineRelease,
            request=pipeline_interface.GetUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateUserPipelineRelease,
                request=pipeline_interface.UpdateUserPipelineReleaseRequest(
                    release=pipeline_release,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserPipelineRelease,
            request=pipeline_interface.UpdateUserPipelineReleaseRequest(
                release=pipeline_release,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_releases(
        self,
        filter_str: str = "",
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
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListUserPipelineReleases,
            request=pipeline_interface.ListUserPipelineReleasesRequest(
                parent=self.target_namespace,
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
    def trigger_pipeline_release(
        self,
        name: str,
        release_id: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerUserPipelineReleaseResponse:
        request = pipeline_interface.TriggerUserPipelineReleaseRequest(
            name=f"users/{self.target_namespace}/pipelines/{name}/releases/{release_id}",
        )
        for input_value in inputs:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.inputs.append(trigger_inputs)
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerUserPipelineRelease,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserPipelineRelease,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_pipeline_release(
        self,
        name: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncUserPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncUserPipelineRelease,
                request=pipeline_interface.TriggerAsyncUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    inputs=inputs,
                    data=data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncUserPipelineRelease,
            request=pipeline_interface.TriggerAsyncUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                inputs=inputs,
                data=data,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_secret(
        self,
        name: str,
        value: str,
        async_enabled: bool = False,
    ) -> secret_interface.CreateUserSecretResponse:
        secret = secret_interface.Secret(id=name, value=value)
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateUserSecret,
                request=secret_interface.CreateUserSecretRequest(
                    secret=secret,
                    parent=self.target_namespace,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateUserSecret,
            request=secret_interface.CreateUserSecretRequest(
                secret=secret,
                parent=self.target_namespace,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_secret(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> secret_interface.GetUserSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserSecret,
                request=secret_interface.GetUserSecretRequest(
                    name=f"{self.target_namespace}/secrets/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserSecret,
            request=secret_interface.GetUserSecretRequest(
                name=f"{self.target_namespace}/secrets/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_secrets(
        self,
        secret: secret_interface.Secret,
        async_enabled: bool = False,
    ) -> secret_interface.UpdateUserSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateUserSecret,
                request=secret_interface.UpdateUserSecretRequest(
                    secret=secret,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserSecret,
            request=secret_interface.UpdateUserSecretRequest(
                secret=secret,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_secret(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> secret_interface.DeleteUserSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserSecret,
                request=secret_interface.DeleteUserSecretRequest(
                    name=f"{self.target_namespace}/secrets/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserSecret,
            request=secret_interface.DeleteUserSecretRequest(
                name=f"{self.target_namespace}/secrets/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_secrets(
        self,
        next_page_token: str = "",
        total_size: int = 100,
        async_enabled: bool = False,
    ) -> secret_interface.ListUserSecretsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListUserSecrets,
                request=secret_interface.ListUserSecretsRequest(
                    parent=self.target_namespace,
                    page_size=total_size,
                    page_token=next_page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListUserSecrets,
            request=secret_interface.ListUserSecretsRequest(
                parent=self.target_namespace,
                page_size=total_size,
                page_token=next_page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    ######## organization endpoints

    @grpc_handler
    def create_org_pipeline(
        self,
        name: str,
        description: str,
        recipe: dict,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateOrganizationPipelineResponse:
        pipeline = pipeline_interface.Pipeline(
            id=name,
            description=description,
        )
        pipeline.recipe.update(recipe)

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
    ) -> pipeline_interface.GetOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganizationPipeline,
                request=pipeline_interface.GetOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationPipeline,
            request=pipeline_interface.GetOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
        pipeline_id: str,
        pipeline_description: str,
        pipeline_documentation_url: str,
        pipeline_license: str,
        pipeline_profile_image: str,
        pipeline_sharing_enabled: bool = False,
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateOrganizationPipelineResponse:
        tags = tags if tags is not None else []
        sharing = common_pb2.Sharing()
        sharing.User.enabled = pipeline_sharing_enabled
        sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        pipeline = pipeline_interface.Pipeline(
            id=pipeline_id,
            description=pipeline_description,
            documentation_url=pipeline_documentation_url,
            license=pipeline_license,
            profile_image=pipeline_profile_image,
            sharing=sharing,
            tags=tags,
        )

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateOrganizationPipeline,
                request=pipeline_interface.UpdateOrganizationPipelineRequest(
                    pipeline=pipeline,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationPipeline,
            request=pipeline_interface.UpdateOrganizationPipelineRequest(
                pipeline=pipeline,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def validate_org_pipeline(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.ValidateOrganizationPipelineResponse:
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
    def clone_org_pipeline(
        self,
        name: str,
        target: str,
        description: str,
        sharing_enabled: bool = False,
        sharing_role_executor: bool = True,
        async_enabled: bool = False,
    ) -> pipeline_interface.CloneOrganizationPipelineResponse:
        sharing = common_pb2.Sharing()
        sharing.User.enabled = sharing_enabled
        if sharing_role_executor:
            sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CloneOrganizationPipeline,
                request=pipeline_interface.CloneOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    target=f"{self.target_namespace}/pipelines/{target}",
                    description=description,
                    sharing=sharing,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CloneOrganizationPipeline,
            request=pipeline_interface.CloneOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                target=f"{self.target_namespace}/pipelines/{target}",
                description=description,
                sharing=sharing,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_org_pipeline(
        self,
        name: str,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerOrganizationPipelineResponse:
        request = pipeline_interface.TriggerOrganizationPipelineRequest(
            name=f"{self.target_namespace}/pipelines/{name}",
        )

        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationPipeline,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationPipeline,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_org_async_pipeline(
        self,
        name: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncOrganizationPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncOrganizationPipeline,
                request=pipeline_interface.TriggerAsyncOrganizationPipelineRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    inputs=inputs,
                    data=data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncOrganizationPipeline,
            request=pipeline_interface.TriggerAsyncOrganizationPipelineRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                inputs=inputs,
                data=data,
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
        visibility: pipeline_interface.Pipeline.Visibility.ValueType,
        order_by: str,
        filter_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListOrganizationPipelinesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOrganizationPipelines,
                request=pipeline_interface.ListOrganizationPipelinesRequest(
                    visibility=visibility,
                    order_by=order_by,
                    parent=self.target_namespace,
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationPipelines,
            request=pipeline_interface.ListOrganizationPipelinesRequest(
                visibility=visibility,
                order_by=order_by,
                parent=self.target_namespace,
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationPipelineRelease,
            request=pipeline_interface.GetOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateOrganizationPipelineRelease,
                request=pipeline_interface.UpdateOrganizationPipelineReleaseRequest(
                    release=pipeline_release,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationPipelineRelease,
            request=pipeline_interface.UpdateOrganizationPipelineReleaseRequest(
                release=pipeline_release,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_org_pipeline_releases(
        self,
        filter_str: str = "",
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
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationPipelineReleases,
            request=pipeline_interface.ListOrganizationPipelineReleasesRequest(
                parent=self.target_namespace,
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
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
    def trigger_org_pipeline_release(
        self,
        name: str,
        release_id: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerOrganizationPipelineReleaseResponse:
        request = pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
            name=f"{self.target_namespace}/pipelines/{name}/releases/{release_id}",
        )
        for input_value in inputs:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.inputs.append(trigger_inputs)
        for d in data:
            trigger_data = pipeline_interface.TriggerData()
            trigger_data.variable.update(d)
            request.data.append(trigger_data)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationPipelineRelease,
                request=request,
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationPipelineRelease,
            request=request,
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_org_pipeline_release(
        self,
        name: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerAsyncOrganizationPipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncOrganizationPipelineRelease,
                request=pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    inputs=inputs,
                    data=data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[
                self.instance
            ].client.TriggerAsyncOrganizationPipelineRelease,
            request=pipeline_interface.TriggerOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                inputs=inputs,
                data=data,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_org_secret(
        self,
        name: str,
        value: str,
        async_enabled: bool = False,
    ) -> secret_interface.CreateOrganizationSecretResponse:
        secret = secret_interface.Secret(id=name, value=value)
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateOrganizationSecret,
                request=secret_interface.CreateUserSecretRequest(
                    secret=secret,
                    parent=self.target_namespace,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateOrganizationSecret,
            request=secret_interface.CreateUserSecretRequest(
                secret=secret,
                parent=self.target_namespace,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_org_secret(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> secret_interface.GetOrganizationSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganizationSecret,
                request=secret_interface.GetOrganizationSecretRequest(
                    name=f"{self.target_namespace}/secrets/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationSecret,
            request=secret_interface.GetOrganizationSecretRequest(
                name=f"{self.target_namespace}/secrets/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_org_secrets(
        self,
        secret: secret_interface.Secret,
        async_enabled: bool = False,
    ) -> secret_interface.UpdateOrganizationSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateOrganizationSecret,
                request=secret_interface.UpdateOrganizationSecretRequest(
                    secret=secret,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationSecret,
            request=secret_interface.UpdateOrganizationSecretRequest(
                secret=secret,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_org_secret(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> secret_interface.DeleteOrganizationSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteOrganizationSecret,
                request=secret_interface.DeleteOrganizationSecretRequest(
                    name=f"{self.target_namespace}/secrets/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationSecret,
            request=secret_interface.DeleteOrganizationSecretRequest(
                name=f"{self.target_namespace}/secrets/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_org_secrets(
        self,
        next_page_token: str = "",
        total_size: int = 100,
        async_enabled: bool = False,
    ) -> secret_interface.ListOrganizationSecretsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOrganizationSecrets,
                request=secret_interface.ListOrganizationSecretsRequest(
                    parent=self.target_namespace,
                    page_size=total_size,
                    page_token=next_page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationSecrets,
            request=secret_interface.ListOrganizationSecretsRequest(
                parent=self.target_namespace,
                page_size=total_size,
                page_token=next_page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_hub_stats(
        self,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetHubStatsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetHubStats,
                request=pipeline_interface.GetHubStatsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetHubStats,
            request=pipeline_interface.GetHubStatsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def clone_pipeline_release(
        self,
        name: str,
        target: str,
        description: str,
        sharing_enabled: bool = False,
        sharing_role_executor: bool = True,
        async_enabled: bool = False,
    ) -> pipeline_interface.CloneUserPipelineReleaseResponse:
        sharing = common_pb2.Sharing()
        sharing.User.enabled = sharing_enabled
        if sharing_role_executor:
            sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CloneUserPipelineRelease,
                request=pipeline_interface.CloneUserPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    target=f"{self.target_namespace}/pipelines/{target}",
                    description=description,
                    sharing=sharing,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CloneUserPipelineRelease,
            request=pipeline_interface.CloneUserPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                target=f"{self.target_namespace}/pipelines/{target}",
                description=description,
                sharing=sharing,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_pipeline_with_stream(
        self,
        name: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerUserPipelineWithStreamResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerUserPipelineWithStream,
                request=pipeline_interface.TriggerUserPipelineWithStreamRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    inputs=inputs,
                    data=data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserPipelineWithStream,
            request=pipeline_interface.TriggerUserPipelineWithStreamRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                inputs=inputs,
                data=data,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def clone_organization_pipeline_release(
        self,
        name: str,
        target: str,
        description: str,
        sharing_enabled: bool = False,
        sharing_role_executor: bool = True,
        async_enabled: bool = False,
    ) -> pipeline_interface.CloneOrganizationPipelineReleaseResponse:
        sharing = common_pb2.Sharing()
        sharing.User.enabled = sharing_enabled
        if sharing_role_executor:
            sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.CloneOrganizationPipelineRelease,
                request=pipeline_interface.CloneOrganizationPipelineReleaseRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    target=f"{self.target_namespace}/pipelines/{target}",
                    description=description,
                    sharing=sharing,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CloneOrganizationPipelineRelease,
            request=pipeline_interface.CloneOrganizationPipelineReleaseRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                target=f"{self.target_namespace}/pipelines/{target}",
                description=description,
                sharing=sharing,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_organization_pipeline_stream(
        self,
        name: str,
        inputs: list,
        data: list,
        async_enabled: bool = False,
    ) -> pipeline_interface.TriggerOrganizationPipelineStreamResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationPipelineStream,
                request=pipeline_interface.TriggerOrganizationPipelineStreamRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    inputs=inputs,
                    data=data,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationPipelineStream,
            request=pipeline_interface.TriggerOrganizationPipelineStreamRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                inputs=inputs,
                data=data,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_connector_definitions(
        self,
        total_size: int = 100,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> component_definition.ListConnectorDefinitionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListConnectorDefinitions,
                request=component_definition.ListConnectorDefinitionsRequest(
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListConnectorDefinitions,
            request=component_definition.ListConnectorDefinitionsRequest(
                view=component_definition.ComponentDefinition.VIEW_FULL,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_connector_definition(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> component_definition.GetConnectorDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetConnectorDefinition,
                request=component_definition.GetConnectorDefinitionRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetConnectorDefinition,
            request=component_definition.GetConnectorDefinitionRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=component_definition.ComponentDefinition.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_operator_definitions(
        self,
        total_size: int = 100,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> component_definition.ListOperatorDefinitionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOperatorDefinitions,
                request=component_definition.ListOperatorDefinitionsRequest(
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListOperatorDefinitions,
            request=component_definition.ListOperatorDefinitionsRequest(
                view=component_definition.ComponentDefinition.VIEW_FULL,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_component_definitions(
        self,
        page: int,
        total_size: int = 100,
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> component_definition.ListComponentDefinitionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListComponentDefinitions,
                request=component_definition.ListComponentDefinitionsRequest(
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListComponentDefinitions,
            request=component_definition.ListComponentDefinitionsRequest(
                view=component_definition.ComponentDefinition.VIEW_FULL,
                page=page,
                page_size=total_size,
                filter=filter_str,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_operator_definition(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> component_definition.GetOperatorDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOperatorDefinition,
                request=component_definition.GetOperatorDefinitionRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOperatorDefinition,
            request=component_definition.GetOperatorDefinitionRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
                view=component_definition.ComponentDefinition.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def check_name(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> common_pb2.CheckNameResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CheckName,
                request=common_pb2.CheckNameRequest(
                    name=f"{self.target_namespace}/pipelines/{name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CheckName,
            request=common_pb2.CheckNameRequest(
                name=f"{self.target_namespace}/pipelines/{name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_runs(
        self,
        namespace_id: str,
        pipeline_id: str,
        page: int = 0,
        total_size: int = 10,
        filter_str: str = "",
        order_by: str = "",
        async_enabled: bool = False,
    ) -> pipeline_interface.ListPipelineRunsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListPipelineRuns,
                request=pipeline_interface.ListPipelineRunsRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                    order_by=order_by,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListPipelineRuns,
            request=pipeline_interface.ListPipelineRunsRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                page=page,
                page_size=total_size,
                filter=filter_str,
                order_by=order_by,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_component_runs(
        self,
        pipeline_run_id: str,
        page: int = 0,
        total_size: int = 10,
        filter_str: str = "",
        order_by: str = "",
        async_enabled: bool = False,
    ) -> pipeline_interface.ListComponentRunsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListComponentRuns,
                request=pipeline_interface.ListComponentRunsRequest(
                    pipeline_run_id=pipeline_run_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                    order_by=order_by,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListComponentRuns,
            request=pipeline_interface.ListComponentRunsRequest(
                pipeline_run_id=pipeline_run_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                page=page,
                page_size=total_size,
                filter=filter_str,
                order_by=order_by,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_namespace_connections(
        self,
        namespace_id: str,
        total_size: int = 10,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> integration_interface.ListNamespaceConnectionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListNamespaceConnections,
                request=integration_interface.ListNamespaceConnectionsRequest(
                    namespace_id=namespace_id,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListNamespaceConnections,
            request=integration_interface.ListNamespaceConnectionsRequest(
                namespace_id=namespace_id,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_namespace_connection(
        self,
        namespace_id: str,
        connection_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.GetNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetNamespaceConnection,
                request=integration_interface.GetNamespaceConnectionRequest(
                    namespace_id=namespace_id,
                    connection_id=connection_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetNamespaceConnection,
            request=integration_interface.GetNamespaceConnectionRequest(
                namespace_id=namespace_id,
                connection_id=connection_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_namespace_connection(
        self,
        connection: integration_interface.Connection,
        async_enabled: bool = False,
    ) -> integration_interface.CreateNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateNamespaceConnection,
                request=integration_interface.CreateNamespaceConnectionRequest(
                    connection=connection,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateNamespaceConnection,
            request=integration_interface.CreateNamespaceConnectionRequest(
                connection=connection,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_namespace_connection(
        self,
        connection: integration_interface.Connection,
        async_enabled: bool = False,
    ) -> integration_interface.UpdateNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateNamespaceConnection,
                request=integration_interface.UpdateNamespaceConnectionRequest(
                    connection=connection,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateNamespaceConnection,
            request=integration_interface.UpdateNamespaceConnectionRequest(
                connection=connection,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_namespace_connection(
        self,
        namespace_id: str,
        connection_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.DeleteNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteNamespaceConnection,
                request=integration_interface.DeleteNamespaceConnectionRequest(
                    namespace_id=namespace_id,
                    connection_id=connection_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteNamespaceConnection,
            request=integration_interface.DeleteNamespaceConnectionRequest(
                namespace_id=namespace_id,
                connection_id=connection_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def test_namespace_connection(
        self,
        namespace_id: str,
        connection_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.TestNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TestNamespaceConnection,
                request=integration_interface.TestNamespaceConnectionRequest(
                    namespace_id=namespace_id,
                    connection_id=connection_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TestNamespaceConnection,
            request=integration_interface.TestNamespaceConnectionRequest(
                namespace_id=namespace_id,
                connection_id=connection_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_integrations(
        self,
        total_size: int = 10,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> integration_interface.ListIntegrationsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListIntegrations,
                request=integration_interface.ListIntegrationsRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListIntegrations,
            request=integration_interface.ListIntegrationsRequest(
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_integration(
        self,
        integration_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.GetIntegrationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetIntegration,
                request=integration_interface.GetIntegrationRequest(
                    integration_id=integration_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetIntegration,
            request=integration_interface.GetIntegrationRequest(
                integration_id=integration_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

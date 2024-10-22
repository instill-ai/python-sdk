# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from datetime import datetime
from typing import Callable, List, Optional

from google.protobuf import field_mask_pb2, timestamp_pb2
from google.protobuf.struct_pb2 import Struct

import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
import instill.protogen.vdp.pipeline.v1beta.component_definition_pb2 as component_definition
import instill.protogen.vdp.pipeline.v1beta.integration_pb2 as integration_interface

# pipeline
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
import instill.protogen.vdp.pipeline.v1beta.pipeline_public_service_pb2_grpc as pipeline_service
import instill.protogen.vdp.pipeline.v1beta.secret_pb2 as secret_interface
from instill.clients.base import Client, RequestFactory
from instill.clients.instance import InstillInstance
from instill.helpers.const import HOST_URL_PROD
from instill.protogen.vdp.pipeline.v1beta import common_pb2
from instill.utils.error_handler import grpc_handler


class PipelineClient(Client):
    def __init__(
        self,
        api_token: str,
        lookup_func: Callable[[str], str],
        url: str = HOST_URL_PROD,
        secure: bool = True,
        requester_id: str = "",
        async_enabled: bool = False,
    ) -> None:
        self.host: InstillInstance = InstillInstance(
            pipeline_service.PipelinePublicServiceStub,
            url=url,
            token=api_token,
            secure=secure,
            async_enabled=async_enabled,
        )
        self.metadata = []

        if requester_id != "":
            requester_uid = lookup_func(requester_id)
            self.metadata = [("instill-requester-uid", requester_uid)]

    def close(self):
        if self.is_serving():
            self.host.channel.close()

    async def async_close(self):
        if self.is_serving():
            self.host.channel.close()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host: InstillInstance):
        self._host = host

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: List[tuple]):
        self._metadata = metadata

    def liveness(
        self, async_enabled: bool = False
    ) -> pipeline_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Liveness,
                request=pipeline_interface.LivenessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Liveness,
            request=pipeline_interface.LivenessRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    def readiness(
        self, async_enabled: bool = False
    ) -> pipeline_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Readiness,
                request=pipeline_interface.ReadinessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Readiness,
            request=pipeline_interface.ReadinessRequest(),
            metadata=self.host.metadata + self.metadata,
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
    def get_hub_stats(
        self,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetHubStatsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetHubStats,
                request=pipeline_interface.GetHubStatsRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetHubStats,
            request=pipeline_interface.GetHubStatsRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def lookup_pipeline(
        self,
        pipeline_uid: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.LookUpPipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.LookUpPipeline,
                request=pipeline_interface.LookUpPipelineRequest(
                    permalink=f"pipelines/{pipeline_uid}",
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.LookUpPipeline,
            request=pipeline_interface.LookUpPipelineRequest(
                permalink=f"pipelines/{pipeline_uid}",
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_public_pipelines(
        self,
        order_by: str = "",
        is_public: bool = True,
        filter_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListPipelinesResponse:
        visibility = (
            pipeline_interface.Pipeline.Visibility.VISIBILITY_PUBLIC
            if is_public
            else pipeline_interface.Pipeline.Visibility.VISIBILITY_PRIVATE
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListPipelines,
                request=pipeline_interface.ListPipelinesRequest(
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.ListPipelines,
            request=pipeline_interface.ListPipelinesRequest(
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                visibility=visibility,
                order_by=order_by,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_pipelines(
        self,
        namespace_id: str,
        order_by: str = "",
        is_public: bool = True,
        filter_str: str = "",
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        async_enabled: bool = False,
    ) -> pipeline_interface.ListNamespacePipelinesResponse:
        visibility = (
            pipeline_interface.Pipeline.Visibility.VISIBILITY_PUBLIC
            if is_public
            else pipeline_interface.Pipeline.Visibility.VISIBILITY_PRIVATE
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListNamespacePipelines,
                request=pipeline_interface.ListNamespacePipelinesRequest(
                    namespace_id=namespace_id,
                    filter=filter_str,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        return RequestFactory(
            method=self.host.client.ListNamespacePipelines,
            request=pipeline_interface.ListNamespacePipelinesRequest(
                namespace_id=namespace_id,
                filter=filter_str,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                visibility=visibility,
                order_by=order_by,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        description: str,
        recipe: Optional[dict] = None,
        raw_recipe: str = "",
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateNamespacePipelineResponse:
        pipeline = pipeline_interface.Pipeline(
            id=pipeline_id,
            description=description,
            raw_recipe=raw_recipe,
        )
        if recipe is None:
            recipe = {}
        pipeline.recipe.update(recipe)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateNamespacePipeline,
                request=pipeline_interface.CreateNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline=pipeline,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateNamespacePipeline,
            request=pipeline_interface.CreateNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline=pipeline,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetNamespacePipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespacePipeline,
                request=pipeline_interface.GetNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespacePipeline,
            request=pipeline_interface.GetNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        description: str,
        recipe: Optional[dict] = None,
        raw_recipe: str = "",
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateNamespacePipelineResponse:

        pipeline = pipeline_interface.Pipeline(
            name=f"namespaces/{namespace_id}/models/{pipeline_id}",
            id=pipeline_id,
            description=description,
            raw_recipe=raw_recipe,
        )

        if recipe is None:
            recipe = {}
        pipeline.recipe.update(recipe)

        update_mask = field_mask_pb2.FieldMask()
        update_mask.paths.extend(
            [
                "description",
                "recipe",
                "raw_recipe",
            ]
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateNamespacePipeline,
                request=pipeline_interface.UpdateNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    pipeline=pipeline,
                    update_mask=update_mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateNamespacePipeline,
            request=pipeline_interface.UpdateNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                pipeline=pipeline,
                update_mask=update_mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteNamespacePipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteNamespacePipeline,
                request=pipeline_interface.DeleteNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteNamespacePipeline,
            request=pipeline_interface.DeleteNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def validate_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.ValidateNamespacePipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ValidateNamespacePipeline,
                request=pipeline_interface.ValidateNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ValidateNamespacePipeline,
            request=pipeline_interface.ValidateNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def rename_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        new_pipeline_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.RenameNamespacePipelineResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.RenameNamespacePipeline,
                request=pipeline_interface.RenameNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    new_pipeline_id=new_pipeline_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.RenameNamespacePipeline,
            request=pipeline_interface.RenameNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                new_pipeline_id=new_pipeline_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def clone_pipeline(
        self,
        namespace_id: str,
        pipeline_id: str,
        target: str,
        description: str,
        sharing_enabled: bool = False,
        sharing_role_executor: bool = True,
        async_enabled: bool = False,
    ) -> pipeline_interface.CloneNamespacePipelineResponse:
        sharing = common_pb2.Sharing()
        sharing.User.enabled = sharing_enabled
        if sharing_role_executor:
            sharing.User.role = common_pb2.Role.ROLE_EXECUTOR

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CloneNamespacePipeline,
                request=pipeline_interface.CloneNamespacePipelineRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    description=description,
                    sharing=sharing,
                    target_namespace_id=namespace_id,
                    target_pipeline_id=target,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CloneNamespacePipeline,
            request=pipeline_interface.CloneNamespacePipelineRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                description=description,
                sharing=sharing,
                target_namespace_id=namespace_id,
                target_pipeline_id=target,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def send_pipeline_event(
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
                method=self.host.async_client.SendNamespacePipelineEvent,
                request=pipeline_interface.SendNamespacePipelineEventRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    event=event,
                    code=code,
                    data=trigger_data,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.SendNamespacePipelineEvent,
            request=pipeline_interface.SendNamespacePipelineEventRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                event=event,
                code=code,
                data=trigger_data,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def send_pipeline_release_event(
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
                method=self.host.async_client.SendNamespacePipelineReleaseEvent,
                request=pipeline_interface.SendNamespacePipelineReleaseEventRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    event=event,
                    code=code,
                    data=data,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.SendNamespacePipelineReleaseEvent,
            request=pipeline_interface.SendNamespacePipelineReleaseEventRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                event=event,
                code=code,
                data=data,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger(
        self,
        namespace_id: str,
        pipeline_id: str,
        data: List[dict],
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
                method=self.host.async_client.TriggerNamespacePipeline,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespacePipeline,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_with_stream(
        self,
        namespace_id: str,
        pipeline_id: str,
        data: List[dict],
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
                method=self.host.async_client.TriggerNamespacePipelineWithStream,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespacePipelineWithStream,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async(
        self,
        namespace_id: str,
        pipeline_id: str,
        data: List[dict],
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
                method=self.host.async_client.TriggerAsyncNamespacePipeline,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerAsyncNamespacePipeline,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        name: str = "",
        description: str = "",
        alias: str = "",
        recipe: Optional[dict] = None,
        raw_recipe: str = "",
        metadata: Optional[dict] = None,
        async_enabled: bool = False,
    ) -> pipeline_interface.CreateNamespacePipelineReleaseResponse:
        release = pipeline_interface.PipelineRelease(
            id=release_id,
            name=name,
            description=description,
            alias=alias,
            raw_recipe=raw_recipe,
        )

        if recipe is None:
            recipe = {}
        release.recipe.update(recipe)
        if metadata is None:
            metadata = {}
        release.metadata.update(metadata)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateNamespacePipelineRelease,
                request=pipeline_interface.CreateNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release=release,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateNamespacePipelineRelease,
            request=pipeline_interface.CreateNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release=release,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_releases(
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
                method=self.host.async_client.ListNamespacePipelineReleases,
                request=pipeline_interface.ListNamespacePipelineReleasesRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                    show_deleted=show_deleted,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListNamespacePipelineReleases,
            request=pipeline_interface.ListNamespacePipelineReleasesRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
                show_deleted=show_deleted,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetNamespacePipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespacePipelineRelease,
                request=pipeline_interface.GetNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespacePipelineRelease,
            request=pipeline_interface.GetNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        description: str = "",
        recipe: Optional[dict] = None,
        raw_recipe: str = "",
        async_enabled: bool = False,
    ) -> pipeline_interface.UpdateNamespacePipelineReleaseResponse:
        release = pipeline_interface.PipelineRelease(
            name=f"namespaces/{namespace_id}/models/{pipeline_id}/releases/{release_id}",
            id=release_id,
            description=description,
            raw_recipe=raw_recipe,
        )

        if recipe is None:
            recipe = {}
        release.recipe.update(recipe)

        update_mask = field_mask_pb2.FieldMask()
        update_mask.paths.extend(
            [
                "recipe",
                "description",
            ]
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateNamespacePipelineRelease,
                request=pipeline_interface.UpdateNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    release=release,
                    update_mask=update_mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateNamespacePipelineRelease,
            request=pipeline_interface.UpdateNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                release=release,
                update_mask=update_mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_pipeline_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.DeleteNamespacePipelineReleaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteNamespacePipelineRelease,
                request=pipeline_interface.DeleteNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteNamespacePipelineRelease,
            request=pipeline_interface.DeleteNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def clone_pipeline_release(
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
                method=self.host.async_client.CloneNamespacePipelineRelease,
                request=pipeline_interface.CloneNamespacePipelineReleaseRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    release_id=release_id,
                    description=description,
                    sharing=sharing,
                    target_namespace_id=namespace_id,
                    target_pipeline_id=target,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CloneNamespacePipelineRelease,
            request=pipeline_interface.CloneNamespacePipelineReleaseRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                release_id=release_id,
                description=description,
                sharing=sharing,
                target_namespace_id=namespace_id,
                target_pipeline_id=target,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        data: List[dict],
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
                method=self.host.async_client.TriggerNamespacePipelineRelease,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespacePipelineRelease,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_release(
        self,
        namespace_id: str,
        pipeline_id: str,
        release_id: str,
        data: List[dict],
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
                method=self.host.async_client.TriggerAsyncNamespacePipelineRelease,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerAsyncNamespacePipelineRelease,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_secret(
        self,
        namespace_id: str,
        secret_id: str,
        description: str,
        secret_name: str = "",
        value: str = "",
        async_enabled: bool = False,
    ) -> secret_interface.CreateNamespaceSecretResponse:
        secret = secret_interface.Secret(
            id=secret_id, name=secret_name, description=description, value=value
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateNamespaceSecret,
                request=secret_interface.CreateNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret=secret,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateNamespaceSecret,
            request=secret_interface.CreateNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret=secret,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_secrets(
        self,
        namespace_id: str,
        total_size: int = 10,
        next_page_token: str = "",
        async_enabled: bool = False,
    ) -> secret_interface.ListNamespaceSecretsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListNamespaceSecrets,
                request=secret_interface.ListNamespaceSecretsRequest(
                    namespace_id=namespace_id,
                    page_size=total_size,
                    page_token=next_page_token,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListNamespaceSecrets,
            request=secret_interface.ListNamespaceSecretsRequest(
                namespace_id=namespace_id,
                page_size=total_size,
                page_token=next_page_token,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_secret(
        self,
        namespace_id: str,
        secret_id: str,
        async_enabled: bool = False,
    ) -> secret_interface.GetNamespaceSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespaceSecret,
                request=secret_interface.GetNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret_id=secret_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespaceSecret,
            request=secret_interface.GetNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret_id=secret_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_secret(
        self,
        namespace_id: str,
        secret_id: str,
        description: str,
        secret_name: str = "",
        value: str = "",
        async_enabled: bool = False,
    ) -> secret_interface.UpdateNamespaceSecretResponse:
        secret = secret_interface.Secret(
            name=secret_name, description=description, value=value
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateNamespaceSecret,
                request=secret_interface.UpdateNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret_id=secret_id,
                    secret=secret,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateNamespaceSecret,
            request=secret_interface.UpdateNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret_id=secret_id,
                secret=secret,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_secret(
        self,
        namespace_id: str,
        secret_id: str,
        async_enabled: bool = False,
    ) -> secret_interface.DeleteNamespaceSecretResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteNamespaceSecret,
                request=secret_interface.DeleteNamespaceSecretRequest(
                    namespace_id=namespace_id,
                    secret_id=secret_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteNamespaceSecret,
            request=secret_interface.DeleteNamespaceSecretRequest(
                namespace_id=namespace_id,
                secret_id=secret_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListComponentDefinitions,
                request=component_definition.ListComponentDefinitionsRequest(
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListComponentDefinitions,
            request=component_definition.ListComponentDefinitionsRequest(
                view=component_definition.ComponentDefinition.VIEW_FULL,
                page=page,
                page_size=total_size,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_operation(
        self,
        operation_id: str,
        async_enabled: bool = False,
    ) -> pipeline_interface.GetOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetOperation,
                request=pipeline_interface.GetOperationRequest(
                    operation_id=operation_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetOperation,
            request=pipeline_interface.GetOperationRequest(
                operation_id=operation_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListConnectorDefinitions,
                request=component_definition.ListConnectorDefinitionsRequest(
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListConnectorDefinitions,
            request=component_definition.ListConnectorDefinitionsRequest(
                view=component_definition.ComponentDefinition.VIEW_FULL,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_connector_definition(
        self,
        namespace_id: str,
        name: str,
        async_enabled: bool = False,
    ) -> component_definition.GetConnectorDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetConnectorDefinition,
                request=component_definition.GetConnectorDefinitionRequest(
                    name=f"namespaces/{namespace_id}/pipelines/{name}",
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetConnectorDefinition,
            request=component_definition.GetConnectorDefinitionRequest(
                name=f"namespaces/{namespace_id}/pipelines/{name}",
                view=component_definition.ComponentDefinition.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListOperatorDefinitions,
                request=component_definition.ListOperatorDefinitionsRequest(
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListOperatorDefinitions,
            request=component_definition.ListOperatorDefinitionsRequest(
                view=component_definition.ComponentDefinition.VIEW_FULL,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_operator_definition(
        self,
        namespace_id: str,
        name: str,
        async_enabled: bool = False,
    ) -> component_definition.GetOperatorDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetOperatorDefinition,
                request=component_definition.GetOperatorDefinitionRequest(
                    name=f"namespaces/{namespace_id}/pipelines/{name}",
                    view=component_definition.ComponentDefinition.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetOperatorDefinition,
            request=component_definition.GetOperatorDefinitionRequest(
                name=f"namespaces/{namespace_id}/pipelines/{name}",
                view=component_definition.ComponentDefinition.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def check_name(
        self,
        namespace_id: str,
        name: str,
        async_enabled: bool = False,
    ) -> common_pb2.CheckNameResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CheckName,
                request=common_pb2.CheckNameRequest(
                    name=f"namespaces/{namespace_id}/pipelines/{name}",
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CheckName,
            request=common_pb2.CheckNameRequest(
                name=f"namespaces/{namespace_id}/pipelines/{name}",
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListPipelineRuns,
                request=pipeline_interface.ListPipelineRunsRequest(
                    namespace_id=namespace_id,
                    pipeline_id=pipeline_id,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListPipelineRuns,
            request=pipeline_interface.ListPipelineRunsRequest(
                namespace_id=namespace_id,
                pipeline_id=pipeline_id,
                page=page,
                page_size=total_size,
                filter=filter_str,
                order_by=order_by,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListComponentRuns,
                request=pipeline_interface.ListComponentRunsRequest(
                    pipeline_run_id=pipeline_run_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListComponentRuns,
            request=pipeline_interface.ListComponentRunsRequest(
                pipeline_run_id=pipeline_run_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
                page=page,
                page_size=total_size,
                filter=filter_str,
                order_by=order_by,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_pipeline_runs_by_credit_owner(
        self,
        start: datetime,
        stop: datetime,
        page: int = 0,
        total_size: int = 10,
        filter_str: str = "",
        order_by: str = "",
        async_enabled: bool = False,
    ) -> pipeline_interface.ListPipelineRunsByCreditOwnerResponse:
        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start)
        stop_timestamp = timestamp_pb2.Timestamp()
        stop_timestamp.FromDatetime(stop)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListPipelineRunsByCreditOwner,
                request=pipeline_interface.ListPipelineRunsByCreditOwnerRequest(
                    start=start_timestamp,
                    stop=stop_timestamp,
                    page=page,
                    page_size=total_size,
                    filter=filter_str,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListPipelineRunsByCreditOwner,
            request=pipeline_interface.ListPipelineRunsByCreditOwnerRequest(
                start=start_timestamp,
                stop=stop_timestamp,
                page=page,
                page_size=total_size,
                filter=filter_str,
                order_by=order_by,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_connections(
        self,
        namespace_id: str,
        total_size: int = 10,
        next_page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> integration_interface.ListNamespaceConnectionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListNamespaceConnections,
                request=integration_interface.ListNamespaceConnectionsRequest(
                    namespace_id=namespace_id,
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListNamespaceConnections,
            request=integration_interface.ListNamespaceConnectionsRequest(
                namespace_id=namespace_id,
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_connection(
        self,
        namespace_id: str,
        connection_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.GetNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespaceConnection,
                request=integration_interface.GetNamespaceConnectionRequest(
                    namespace_id=namespace_id,
                    connection_id=connection_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespaceConnection,
            request=integration_interface.GetNamespaceConnectionRequest(
                namespace_id=namespace_id,
                connection_id=connection_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_connection(
        self,
        namespace_id: str,
        integration_id: str,
        connection_id: str,
        scopes: Optional[List[str]] = None,
        identity: Optional[str] = None,
        setup: Optional[dict] = None,
        o_auth_access_details: Optional[dict] = None,
        is_oauth: bool = False,
        async_enabled: bool = False,
    ) -> integration_interface.CreateNamespaceConnectionResponse:
        if scopes is None:
            scopes = []
        connection = integration_interface.Connection(
            namespace_id=namespace_id,
            integration_id=integration_id,
            id=connection_id,
            identity=identity,
            scopes=scopes,
        )

        setup = {} if setup is None else setup
        connection.setup.Clear()
        connection.setup.update(setup)
        if o_auth_access_details is None:
            o_auth_access_details = {}
        connection.o_auth_access_details.update(o_auth_access_details)

        if is_oauth:
            connection.method = integration_interface.Connection.Method.METHOD_OAUTH
        else:
            connection.method = (
                integration_interface.Connection.Method.METHOD_DICTIONARY
            )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateNamespaceConnection,
                request=integration_interface.CreateNamespaceConnectionRequest(
                    connection=connection,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateNamespaceConnection,
            request=integration_interface.CreateNamespaceConnectionRequest(
                connection=connection,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_connection(
        self,
        namespace_id: str,
        integration_id: str,
        connection_id: str,
        scopes: Optional[List[str]] = None,
        identity: Optional[str] = None,
        setup: Optional[dict] = None,
        # o_auth_access_details: Optional[dict] = None,
        is_oauth: bool = False,
        async_enabled: bool = False,
    ) -> integration_interface.UpdateNamespaceConnectionResponse:
        if scopes is None:
            scopes = []
        connection = integration_interface.Connection(
            namespace_id=namespace_id,
            integration_id=integration_id,
            scopes=scopes,
            identity=identity,
        )

        if setup is None:
            setup = {}
        connection.setup.Clear()
        connection.setup.update(setup)
        # if o_auth_access_details is None:
        #     o_auth_access_details = {}
        # connection.o_auth_access_details.Clear()
        # connection.o_auth_access_details.update(o_auth_access_details)

        update_mask = field_mask_pb2.FieldMask()
        update_mask.paths.extend(
            [
                "setup",
                "scopes",
                "identity",
            ]
        )

        if is_oauth:
            connection.method = integration_interface.Connection.Method.METHOD_OAUTH
        else:
            connection.method = (
                integration_interface.Connection.Method.METHOD_DICTIONARY
            )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateNamespaceConnection,
                request=integration_interface.UpdateNamespaceConnectionRequest(
                    connection_id=connection_id,
                    connection=connection,
                    update_mask=update_mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateNamespaceConnection,
            request=integration_interface.UpdateNamespaceConnectionRequest(
                connection_id=connection_id,
                connection=connection,
                update_mask=update_mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_connection(
        self,
        namespace_id: str,
        connection_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.DeleteNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteNamespaceConnection,
                request=integration_interface.DeleteNamespaceConnectionRequest(
                    namespace_id=namespace_id,
                    connection_id=connection_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteNamespaceConnection,
            request=integration_interface.DeleteNamespaceConnectionRequest(
                namespace_id=namespace_id,
                connection_id=connection_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def test_connection(
        self,
        namespace_id: str,
        connection_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.TestNamespaceConnectionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TestNamespaceConnection,
                request=integration_interface.TestNamespaceConnectionRequest(
                    namespace_id=namespace_id,
                    connection_id=connection_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TestNamespaceConnection,
            request=integration_interface.TestNamespaceConnectionRequest(
                namespace_id=namespace_id,
                connection_id=connection_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListIntegrations,
                request=integration_interface.ListIntegrationsRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListIntegrations,
            request=integration_interface.ListIntegrationsRequest(
                page_size=total_size,
                page_token=next_page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_integration(
        self,
        integration_id: str,
        async_enabled: bool = False,
    ) -> integration_interface.GetIntegrationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetIntegration,
                request=integration_interface.GetIntegrationRequest(
                    integration_id=integration_id,
                    view=pipeline_interface.Pipeline.VIEW_RECIPE,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetIntegration,
            request=integration_interface.GetIntegrationRequest(
                integration_id=integration_id,
                view=pipeline_interface.Pipeline.VIEW_RECIPE,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

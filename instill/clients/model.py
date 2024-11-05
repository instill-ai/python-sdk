# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from datetime import datetime
from typing import Callable, List, Optional

from google.protobuf import field_mask_pb2, timestamp_pb2
from google.protobuf.struct_pb2 import Struct

import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
import instill.protogen.common.task.v1alpha.task_pb2 as task_interface
import instill.protogen.model.model.v1alpha.model_definition_pb2 as model_definition_interface

# model
import instill.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
from instill.clients.base import Client, RequestFactory
from instill.clients.instance import InstillInstance
from instill.helpers.const import HOST_URL_PROD
from instill.utils.error_handler import grpc_handler


class ModelClient(Client):
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
            model_service.ModelPublicServiceStub,
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
    def metadata(self, metadata: List[tuple]):
        self._metadata = metadata

    def liveness(self, async_enabled: bool = False) -> model_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Liveness,
                request=model_interface.LivenessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Liveness,
            request=model_interface.LivenessRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    def readiness(
        self, async_enabled: bool = False
    ) -> model_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Readiness,
                request=model_interface.ReadinessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Readiness,
            request=model_interface.ReadinessRequest(),
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
    def watch_model(
        self,
        namespace_id: str,
        model_id: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.WatchNamespaceModelResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.WatchNamespaceModel,
                request=model_interface.WatchNamespaceModelRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    version=version,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.WatchNamespaceModel,
            request=model_interface.WatchNamespaceModelRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                version=version,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def watch_latest_model(
        self,
        namespace_id: str,
        model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.WatchNamespaceLatestModelResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.WatchNamespaceLatestModel,
                request=model_interface.WatchNamespaceLatestModelRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.WatchNamespaceLatestModel,
            request=model_interface.WatchNamespaceLatestModelRequest(
                namespace_id=namespace_id,
                model_id=model_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_model(
        self,
        namespace_id: str,
        model_id: str,
        task: task_interface.Task.ValueType,
        region: str,
        hardware: str,
        definition: str = "model-definitions/container",
        configuration: Optional[dict] = None,
        is_public: bool = True,
        async_enabled: bool = False,
    ) -> model_interface.CreateNamespaceModelResponse:

        model = model_interface.Model()
        model.id = model_id
        model.task = task
        model.region = region
        model.hardware = hardware
        model.model_definition = definition
        model.visibility = (
            model_interface.Model.VISIBILITY_PUBLIC
            if is_public
            else model_interface.Model.VISIBILITY_PRIVATE
        )

        configuration = {} if configuration is None else configuration
        model.configuration.Clear()
        model.configuration.update(configuration)
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateNamespaceModel,
                request=model_interface.CreateNamespaceModelRequest(
                    namespace_id=namespace_id,
                    model=model,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateNamespaceModel,
            request=model_interface.CreateNamespaceModelRequest(
                namespace_id=namespace_id,
                model=model,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger(
        self,
        namespace_id: str,
        model_id: str,
        task_inputs: List[dict],
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerNamespaceModelResponse:

        request = model_interface.TriggerNamespaceModelRequest(
            namespace_id=namespace_id,
            model_id=model_id,
            version=version,
        )
        for input_value in task_inputs:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.task_inputs.append(trigger_inputs)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TriggerNamespaceModel,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespaceModel,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async(
        self,
        namespace_id: str,
        model_id: str,
        task_inputs: List[dict],
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerAsyncNamespaceModelResponse:

        request = model_interface.TriggerAsyncNamespaceModelRequest(
            namespace_id=namespace_id,
            model_id=model_id,
            version=version,
        )
        for input_value in task_inputs:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.task_inputs.append(trigger_inputs)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TriggerAsyncNamespaceModel,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerAsyncNamespaceModel,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_latest(
        self,
        namespace_id: str,
        model_id: str,
        task_inputs: List[dict],
        async_enabled: bool = False,
    ) -> model_interface.TriggerNamespaceLatestModelResponse:

        request = model_interface.TriggerNamespaceLatestModelRequest(
            namespace_id=namespace_id,
            model_id=model_id,
        )
        for input_value in task_inputs:
            trigger_input = Struct()
            trigger_input.update(input_value)
            request.task_inputs.append(trigger_input)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TriggerNamespaceLatestModel,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespaceLatestModel,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_latest(
        self,
        namespace_id: str,
        model_id: str,
        task_inputs: List[dict],
        async_enabled: bool = False,
    ) -> model_interface.TriggerAsyncNamespaceLatestModelResponse:

        request = model_interface.TriggerAsyncNamespaceLatestModelRequest(
            namespace_id=namespace_id,
            model_id=model_id,
        )
        for input_value in task_inputs:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.task_inputs.append(trigger_inputs)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TriggerAsyncNamespaceLatestModel,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerAsyncNamespaceLatestModel,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_model_binary_file_upload(
        self,
        namespace_id: str,
        model_id: str,
        task_inputs: List[dict],
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerNamespaceModelBinaryFileUploadResponse:

        request = model_interface.TriggerNamespaceModelBinaryFileUploadRequest(
            namespace_id=namespace_id,
            model_id=model_id,
            version=version,
        )
        for input_value in task_inputs:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.task_input.append(trigger_inputs)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TriggerNamespaceModelBinaryFileUpload,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespaceModelBinaryFileUpload,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def trigger_latest_model_binary_file_upload(
        self,
        namespace_id: str,
        model_id: str,
        task_input: List[dict],
        async_enabled: bool = False,
    ) -> model_interface.TriggerNamespaceLatestModelBinaryFileUploadResponse:

        request = model_interface.TriggerNamespaceLatestModelBinaryFileUploadRequest(
            namespace_id=namespace_id,
            model_id=model_id,
        )
        for input_value in task_input:
            trigger_inputs = Struct()
            trigger_inputs.update(input_value)
            request.task_input.append(trigger_inputs)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.TriggerNamespaceLatestModelBinaryFileUpload,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.TriggerNamespaceLatestModelBinaryFileUpload,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_namespace_model_operation(
        self,
        namespace_id: str,
        model_id: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.GetNamespaceModelOperationResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespaceModelOperation,
                request=model_interface.GetNamespaceModelOperationRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    version=version,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespaceModelOperation,
            request=model_interface.GetNamespaceModelOperationRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                version=version,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_namespace_latest_model_operation(
        self,
        namespace_id: str,
        model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.GetNamespaceLatestModelOperationResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespaceLatestModelOperation,
                request=model_interface.GetNamespaceLatestModelOperationRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespaceLatestModelOperation,
            request=model_interface.GetNamespaceLatestModelOperationRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_model_operation(
        self,
        operation_id: str,
        async_enabled: bool = False,
    ) -> model_interface.GetModelOperationResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetModelOperation,
                request=model_interface.GetModelOperationRequest(
                    operation_id=operation_id,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetModelOperation,
            request=model_interface.GetModelOperationRequest(
                operation_id=operation_id,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_model(
        self,
        namespace_id: str,
        model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.DeleteNamespaceModelResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteNamespaceModel,
                request=model_interface.DeleteNamespaceModelRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteNamespaceModel,
            request=model_interface.DeleteNamespaceModelRequest(
                namespace_id=namespace_id,
                model_id=model_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def rename_model(
        self,
        namespace_id: str,
        model_id: str,
        new_model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.RenameNamespaceModelResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.RenameNamespaceModel,
                request=model_interface.RenameNamespaceModelRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    new_model_id=new_model_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.RenameNamespaceModel,
            request=model_interface.RenameNamespaceModelRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                new_model_id=new_model_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_model(
        self,
        namespace_id: str,
        model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.GetNamespaceModelResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespaceModel,
                request=model_interface.GetNamespaceModelRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespaceModel,
            request=model_interface.GetNamespaceModelRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_model(
        self,
        namespace_id: str,
        model_id: str,
        description: str,
        documentation_url: str,
        hardware: str,
        model_license: str = "",
        is_public: bool = True,
        async_enabled: bool = False,
    ) -> model_interface.UpdateNamespaceModelResponse:

        model = model_interface.Model(
            name=f"namespaces/{namespace_id}/models/{model_id}",
            description=description,
            documentation_url=documentation_url,
            hardware=hardware,
            license=model_license,
            visibility=(
                model_interface.Model.VISIBILITY_PUBLIC
                if is_public
                else model_interface.Model.VISIBILITY_PRIVATE
            ),
        )
        update_mask = field_mask_pb2.FieldMask()
        update_mask.paths.extend(
            [
                "description",
                "documentation_url",
                "hardware",
                "license",
                "visibility",
            ]
        )

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateNamespaceModel,
                request=model_interface.UpdateNamespaceModelRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    model=model,
                    update_mask=update_mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateNamespaceModel,
            request=model_interface.UpdateNamespaceModelRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                model=model,
                update_mask=update_mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def lookup_model(
        self,
        model_uid: str,
        async_enabled: bool = False,
    ) -> model_interface.LookUpModelResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.LookUpModel,
                request=model_interface.LookUpModelRequest(
                    permalink=f"models/{model_uid}"
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.LookUpModel,
            request=model_interface.LookUpModelRequest(permalink=f"models/{model_uid}"),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_models(
        self,
        namespace_id: str,
        is_public: bool = True,
        next_page_token: str = "",
        total_size: int = 10,
        show_deleted: bool = False,
        public=False,
        filter_str: str = "",
        order_by: str = "",
        async_enabled: bool = False,
    ) -> model_interface.ListNamespaceModelsResponse:

        visibility = (
            model_interface.Model.VISIBILITY_PUBLIC
            if is_public
            else model_interface.Model.VISIBILITY_PRIVATE
        )

        if async_enabled:
            if public:
                method = self.host.async_client.ListModels
                return RequestFactory(
                    method=method,
                    request=model_interface.ListModelsRequest(
                        page_size=total_size,
                        page_token=next_page_token,
                        show_deleted=show_deleted,
                        view=model_definition_interface.VIEW_FULL,
                        filter=filter_str,
                        visibility=visibility,
                        order_by=order_by,
                    ),
                    metadata=self.host.metadata + self.metadata,
                ).send_async()
            method = self.host.async_client.ListNamespaceModels
            return RequestFactory(
                method=method,
                request=model_interface.ListNamespaceModelsRequest(
                    namespace_id=namespace_id,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=model_definition_interface.VIEW_FULL,
                    filter=filter_str,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()
        if public:
            method = self.host.client.ListModels
            return RequestFactory(
                method=method,
                request=model_interface.ListModelsRequest(
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=model_definition_interface.VIEW_FULL,
                    filter=filter_str,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_sync()
        method = self.host.client.ListNamespaceModels
        return RequestFactory(
            method=method,
            request=model_interface.ListNamespaceModelsRequest(
                namespace_id=namespace_id,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=model_definition_interface.VIEW_FULL,
                filter=filter_str,
                visibility=visibility,
                order_by=order_by,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_model_definitions(
        self,
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> model_definition_interface.ListModelDefinitionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListModelDefinitions,
                request=model_definition_interface.ListModelDefinitionsRequest(
                    page_size=page_size,
                    page_token=page_token,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListModelDefinitions,
            request=model_definition_interface.ListModelDefinitionsRequest(
                page_size=page_size,
                page_token=page_token,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_available_regions(
        self,
        async_enabled: bool = False,
    ) -> model_interface.ListAvailableRegionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListAvailableRegions,
                request=model_interface.ListAvailableRegionsRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListAvailableRegions,
            request=model_interface.ListAvailableRegionsRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_model_definition(
        self,
        model_definition_id: str,
        async_enabled: bool = False,
    ) -> model_definition_interface.GetModelDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetModelDefinition,
                request=model_definition_interface.GetModelDefinitionRequest(
                    view=model_definition_interface.VIEW_FULL,
                    model_definition_id=model_definition_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetModelDefinition,
            request=model_definition_interface.GetModelDefinitionRequest(
                view=model_definition_interface.VIEW_FULL,
                model_definition_id=model_definition_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_operation(
        self,
        operation_id: str,
        async_enabled: bool = False,
    ) -> model_interface.GetModelOperationResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetModelOperation,
                request=model_interface.GetModelOperationRequest(
                    operation_id=operation_id,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetModelOperation,
            request=model_interface.GetModelOperationRequest(
                operation_id=operation_id,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_latest_model_operation(
        self,
        namespace_id: str,
        model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.GetNamespaceLatestModelOperationResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetNamespaceLatestModelOperation,
                request=model_interface.GetNamespaceLatestModelOperationRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetNamespaceLatestModelOperation,
            request=model_interface.GetNamespaceLatestModelOperationRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_model_versions(
        self,
        namespace_id: str,
        page: int,
        model_id: str,
        page_size: int = 10,
        async_enabled: bool = False,
    ) -> model_interface.ListNamespaceModelVersionsResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListNamespaceModelVersions,
                request=model_interface.ListNamespaceModelVersionsRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    page_size=page_size,
                    page=page,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListNamespaceModelVersions,
            request=model_interface.ListNamespaceModelVersionsRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                page_size=page_size,
                page=page,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_model_version(
        self,
        namespace_id: str,
        model_id: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.DeleteNamespaceModelVersionResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteNamespaceModelVersion,
                request=model_interface.DeleteNamespaceModelVersionRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    version=version,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteNamespaceModelVersion,
            request=model_interface.DeleteNamespaceModelVersionRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                version=version,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_model_runs(
        self,
        namespace_id: str,
        model_id: str,
        page_size: int = 10,
        page: int = 0,
        order_by: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> model_interface.ListModelRunsResponse:

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListModelRuns,
                request=model_interface.ListModelRunsRequest(
                    namespace_id=namespace_id,
                    model_id=model_id,
                    page_size=page_size,
                    page=page,
                    order_by=order_by,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListModelRuns,
            request=model_interface.ListModelRunsRequest(
                namespace_id=namespace_id,
                model_id=model_id,
                page_size=page_size,
                page=page,
                order_by=order_by,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_model_runs_by_requester(
        self,
        start: datetime,
        stop: datetime,
        requester_id: str,
        page_size: int = 10,
        page: int = 0,
        order_by: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> model_interface.ListModelRunsByRequesterResponse:
        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start)
        stop_timestamp = timestamp_pb2.Timestamp()
        stop_timestamp.FromDatetime(stop)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListModelRunsByRequester,
                request=model_interface.ListModelRunsByRequesterRequest(
                    start=start_timestamp,
                    stop=stop_timestamp,
                    requester_id=requester_id,
                    page_size=page_size,
                    page=page,
                    order_by=order_by,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListModelRunsByRequester,
            request=model_interface.ListModelRunsByRequesterRequest(
                start=start_timestamp,
                stop=stop_timestamp,
                requester_id=requester_id,
                page_size=page_size,
                page=page,
                order_by=order_by,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

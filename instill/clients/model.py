# pylint: disable=no-member,wrong-import-position
from typing import Dict

from google.protobuf import field_mask_pb2

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
import instill.protogen.common.task.v1alpha.task_pb2 as task_interface
import instill.protogen.model.model.v1alpha.model_definition_pb2 as model_definition_interface

# model
import instill.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler


class ModelClient(Client):
    def __init__(self, namespace: str, async_enabled: bool) -> None:
        self.hosts: Dict[str, InstillInstance] = {}
        self.namespace: str = namespace
        if DEFAULT_INSTANCE in global_config.hosts:
            self.instance = DEFAULT_INSTANCE
        elif len(global_config.hosts) == 0:
            self.instance = ""
        else:
            self.instance = list(global_config.hosts.keys())[0]

        if global_config.hosts is not None:
            for instance, config in global_config.hosts.items():
                self.hosts[instance] = InstillInstance(
                    model_service.ModelPublicServiceStub,
                    url=config.url,
                    token=config.token,
                    secure=config.secure,
                    async_enabled=async_enabled,
                )

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

    def liveness(self, async_enabled: bool = False) -> model_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Liveness,
                request=model_interface.LivenessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Liveness,
            request=model_interface.LivenessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    def readiness(
        self, async_enabled: bool = False
    ) -> model_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Readiness,
                request=model_interface.ReadinessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Readiness,
            request=model_interface.ReadinessRequest(),
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
    def watch_model(
        self,
        model_name: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.WatchUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.WatchUserModel,
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchUserModel,
            request=model_interface.WatchUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_latest_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.WatchUserLatestModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.WatchUserLatestModel,
                request=model_interface.WatchUserLatestModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchUserLatestModel,
            request=model_interface.WatchUserLatestModelRequest(
                name=f"{self.namespace}/models/{model_name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_model(
        self,
        name: str,
        task: task_interface.Task.ValueType,
        region: str,
        hardware: str,
        definition: str,
        configuration: dict,
        visibility: model_interface.Model.Visibility.ValueType = model_interface.Model.VISIBILITY_PUBLIC,
        async_enabled: bool = False,
    ) -> model_interface.CreateUserModelResponse:
        model = model_interface.Model()
        model.id = name
        model.task = task
        model.region = region
        model.hardware = hardware
        model.model_definition = definition
        model.visibility = visibility
        model.configuration.Clear()
        model.configuration.update(configuration)
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateUserModel,
                request=model_interface.CreateUserModelRequest(
                    model=model, parent=self.namespace
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateUserModel,
            request=model_interface.CreateUserModelRequest(
                model=model, parent=self.namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_model(
        self,
        model_name: str,
        task_inputs: list[model_interface.TaskInput],
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerUserModel,
                request=model_interface.TriggerUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserModel,
            request=model_interface.TriggerUserModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_model(
        self,
        model_name: str,
        task_inputs: list[model_interface.TaskInput],
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerAsyncUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerAsyncUserModel,
                request=model_interface.TriggerAsyncUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncUserModel,
            request=model_interface.TriggerAsyncUserModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_latest_model(
        self,
        model_name: str,
        task_inputs: list[model_interface.TaskInput],
        async_enabled: bool = False,
    ) -> model_interface.TriggerUserLatestModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerUserLatestModel,
                request=model_interface.TriggerUserLatestModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserLatestModel,
            request=model_interface.TriggerUserLatestModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_latest_model(
        self,
        model_name: str,
        task_inputs: list[model_interface.TaskInput],
        async_enabled: bool = False,
    ) -> model_interface.TriggerAsyncUserLatestModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncUserLatestModel,
                request=model_interface.TriggerAsyncUserLatestModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncUserLatestModel,
            request=model_interface.TriggerAsyncUserLatestModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_model_binary_file_upload(
        self,
        model_name: str,
        task_input: model_interface.TaskInputStream,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerUserModelBinaryFileUploadResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerUserModelBinaryFileUpload,
                request=model_interface.TriggerUserModelBinaryFileUploadRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_input=task_input,
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserModelBinaryFileUpload,
            request=model_interface.TriggerUserModelBinaryFileUploadRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_input=task_input,
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.DeleteUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserModel,
                request=model_interface.DeleteUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserModel,
            request=model_interface.DeleteUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def rename_model(
        self,
        model_name: str,
        new_model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.RenameUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.RenameUserModel,
                request=model_interface.RenameUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    new_model_id=new_model_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RenameUserModel,
            request=model_interface.RenameUserModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                new_model_id=new_model_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.GetUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserModel,
                request=model_interface.GetUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserModel,
            request=model_interface.GetUserModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_model(
        self,
        model: model_interface.Model,
        mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> model_interface.UpdateUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateUserModel,
                request=model_interface.UpdateUserModelRequest(
                    model=model,
                    update_mask=mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateUserModel,
            request=model_interface.UpdateUserModelRequest(
                model=model,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def lookup_model(
        self,
        model_uid: str,
        async_enabled: bool = False,
    ) -> model_interface.LookUpModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.LookUpModel,
                request=model_interface.LookUpModelRequest(
                    permalink=f"models/{model_uid}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.LookUpModel,
            request=model_interface.LookUpModelRequest(permalink=f"models/{model_uid}"),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_models(
        self,
        visibility: model_interface.Model.Visibility.ValueType = model_interface.Model.VISIBILITY_PUBLIC,
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        public=False,
        filter_str: str = "",
        order_by: str = "",
        async_enabled: bool = False,
    ) -> model_interface.ListUserModelsResponse:
        if async_enabled:
            if public:
                method = self.hosts[self.instance].async_client.ListModels
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
                    metadata=self.hosts[self.instance].metadata,
                ).send_async()
            method = self.hosts[self.instance].async_client.ListUserModels
            return RequestFactory(
                method=method,
                request=model_interface.ListUserModelsRequest(
                    parent=self.namespace,
                    page_size=total_size,
                    page_token=next_page_token,
                    show_deleted=show_deleted,
                    view=model_definition_interface.VIEW_FULL,
                    filter=filter_str,
                    visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()
        if public:
            method = self.hosts[self.instance].client.ListModels
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
                metadata=self.hosts[self.instance].metadata,
            ).send_sync()
        method = self.hosts[self.instance].client.ListUserModels
        return RequestFactory(
            method=method,
            request=model_interface.ListUserModelsRequest(
                parent=self.namespace,
                page_size=total_size,
                page_token=next_page_token,
                show_deleted=show_deleted,
                view=model_definition_interface.VIEW_FULL,
                filter=filter_str,
                visibility=visibility,
                order_by=order_by,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_model_definitions(
        self,
        page_size: int = 100,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> model_definition_interface.ListModelDefinitionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListModelDefinitions,
                request=model_definition_interface.ListModelDefinitionsRequest(
                    page_size=page_size,
                    page_token=page_token,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListModelDefinitions,
            request=model_definition_interface.ListModelDefinitionsRequest(
                page_size=page_size,
                page_token=page_token,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_available_regions(
        self,
        async_enabled: bool = False,
    ) -> model_interface.ListAvailableRegionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListAvailableRegions,
                request=model_interface.ListAvailableRegionsRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListAvailableRegions,
            request=model_interface.ListAvailableRegionsRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_model_definition(
        self,
        model_definition_id: str,
        async_enabled: bool = False,
    ) -> model_definition_interface.GetModelDefinitionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetModelDefinition,
                request=model_definition_interface.GetModelDefinitionRequest(
                    view=model_definition_interface.VIEW_FULL,
                    model_definition_id=model_definition_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetModelDefinition,
            request=model_definition_interface.GetModelDefinitionRequest(
                view=model_definition_interface.VIEW_FULL,
                model_definition_id=model_definition_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_operation(
        self,
        operation_id: str,
        async_enabled: bool = False,
    ) -> model_interface.GetModelOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetModelOperation,
                request=model_interface.GetModelOperationRequest(
                    operation_id=operation_id,
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetModelOperation,
            request=model_interface.GetModelOperationRequest(
                operation_id=operation_id,
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_latest_model_operation(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.GetUserLatestModelOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.GetUserLatestModelOperation,
                request=model_interface.GetUserLatestModelOperationRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserLatestModelOperation,
            request=model_interface.GetUserLatestModelOperationRequest(
                name=f"{self.namespace}/models/{model_name}",
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_organization_latest_model_operation(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.GetOrganizationLatestModelOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.GetOrganizationLatestModelOperation,
                request=model_interface.GetOrganizationLatestModelOperationRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationLatestModelOperation,
            request=model_interface.GetOrganizationLatestModelOperationRequest(
                name=f"{self.namespace}/models/{model_name}",
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_model_versions(
        self,
        page: int,
        model_name: str,
        page_size: int = 100,
        async_enabled: bool = False,
    ) -> model_interface.ListUserModelVersionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListUserModelVersions,
                request=model_interface.ListUserModelVersionsRequest(
                    page_size=page_size,
                    page=page,
                    name=f"{self.namespace}/models/{model_name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListUserModelVersions,
            request=model_interface.ListUserModelVersionsRequest(
                page_size=page_size,
                page=page,
                name=f"{self.namespace}/models/{model_name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_model_version(
        self,
        model_name: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.DeleteUserModelVersionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteUserModelVersion,
                request=model_interface.DeleteUserModelVersionRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteUserModelVersion,
            request=model_interface.DeleteUserModelVersionRequest(
                name=f"{self.namespace}/models/{model_name}",
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_organization_models(
        self,
        page_size: int = 100,
        page_token: str = "",
        parent: str = "",
        show_deleted: bool = False,
        # filter: str = "",
        order_by: str = "",
        async_enabled: bool = False,
    ) -> model_interface.ListOrganizationModelsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListOrganizationModels,
                request=model_interface.ListOrganizationModelsRequest(
                    page_size=page_size,
                    page_token=page_token,
                    view=model_definition_interface.VIEW_FULL,
                    parent=parent,
                    show_deleted=show_deleted,
                    # filter=filter,
                    # visibility=visibility,
                    order_by=order_by,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationModels,
            request=model_interface.ListOrganizationModelsRequest(
                page_size=page_size,
                page_token=page_token,
                view=model_definition_interface.VIEW_FULL,
                parent=parent,
                show_deleted=show_deleted,
                # filter=filter,
                # visibility=visibility,
                order_by=order_by,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_organization_model(
        self,
        name: str,
        definition: str,
        configuration: dict,
        parent: str,
        async_enabled: bool = False,
    ) -> model_interface.CreateOrganizationModelResponse:
        model = model_interface.Model()
        model.id = name
        model.model_definition = definition
        model.configuration.update(configuration)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateOrganizationModel,
                request=model_interface.CreateOrganizationModelRequest(
                    model=model,
                    parent=parent,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateOrganizationModel,
            request=model_interface.CreateOrganizationModelRequest(
                model=model,
                parent=parent,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_organization_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.GetOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetOrganizationModel,
                request=model_interface.GetOrganizationModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    view=model_definition_interface.VIEW_FULL,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetOrganizationModel,
            request=model_interface.GetOrganizationModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_organization_model(
        self,
        model: model_interface.Model,
        update_mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> model_interface.UpdateOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateOrganizationModel,
                request=model_interface.UpdateOrganizationModelRequest(
                    model=model,
                    update_mask=update_mask,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateOrganizationModel,
            request=model_interface.UpdateOrganizationModelRequest(
                model=model,
                update_mask=update_mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_organization_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.DeleteOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteOrganizationModel,
                request=model_interface.DeleteOrganizationModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationModel,
            request=model_interface.DeleteOrganizationModelRequest(
                name=f"{self.namespace}/models/{model_name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def rename_organization_model(
        self,
        model_name: str,
        new_model_id: str,
        async_enabled: bool = False,
    ) -> model_interface.RenameOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.RenameOrganizationModel,
                request=model_interface.RenameOrganizationModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    new_model_id=new_model_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RenameOrganizationModel,
            request=model_interface.RenameOrganizationModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                new_model_id=new_model_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_organization_model(
        self,
        model_name: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.WatchOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.WatchOrganizationModel,
                request=model_interface.WatchOrganizationModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchOrganizationModel,
            request=model_interface.WatchOrganizationModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def watch_organization_latest_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.WatchOrganizationLatestModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.WatchOrganizationLatestModel,
                request=model_interface.WatchOrganizationLatestModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.WatchOrganizationLatestModel,
            request=model_interface.WatchOrganizationLatestModelRequest(
                name=f"{self.namespace}/models/{model_name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_organization_model_versions(
        self,
        page_size: int,
        page: int,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.ListOrganizationModelVersionsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.ListOrganizationModelVersions,
                request=model_interface.ListOrganizationModelVersionsRequest(
                    page_size=page_size,
                    page=page,
                    name=f"{self.namespace}/models/{model_name}",
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListOrganizationModelVersions,
            request=model_interface.ListOrganizationModelVersionsRequest(
                page_size=page_size,
                page=page,
                name=f"{self.namespace}/models/{model_name}",
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_organization_model_version(
        self,
        model_name: str,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.DeleteOrganizationModelVersionResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.DeleteOrganizationModelVersion,
                request=model_interface.DeleteOrganizationModelVersionRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteOrganizationModelVersion,
            request=model_interface.DeleteOrganizationModelVersionRequest(
                name=f"{self.namespace}/models/{model_name}",
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_organization_model(
        self,
        model_name: str,
        task_inputs: list,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerOrganizationModel,
                request=model_interface.TriggerOrganizationModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationModel,
            request=model_interface.TriggerOrganizationModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_organization_model(
        self,
        model_name: str,
        task_inputs: list,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerAsyncOrganizationModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncOrganizationModel,
                request=model_interface.TriggerAsyncOrganizationModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncOrganizationModel,
            request=model_interface.TriggerAsyncOrganizationModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_organization_latest_model(
        self,
        model_name: str,
        task_inputs: list,
        async_enabled: bool = False,
    ) -> model_interface.TriggerOrganizationLatestModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationLatestModel,
                request=model_interface.TriggerOrganizationLatestModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerOrganizationLatestModel,
            request=model_interface.TriggerOrganizationLatestModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_async_organization_latest_model(
        self,
        model_name: str,
        task_inputs: list,
        async_enabled: bool = False,
    ) -> model_interface.TriggerAsyncOrganizationLatestModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerAsyncOrganizationLatestModel,
                request=model_interface.TriggerAsyncOrganizationLatestModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerAsyncOrganizationLatestModel,
            request=model_interface.TriggerAsyncOrganizationLatestModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                task_inputs=task_inputs,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_organization_model_binary_file_upload(
        self,
        model_name: str,
        # task_input: list,
        version: str,
        async_enabled: bool = False,
    ) -> model_interface.TriggerOrganizationModelBinaryFileUploadResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.TriggerOrganizationModelBinaryFileUpload,
                request=model_interface.TriggerOrganizationModelBinaryFileUploadRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    # task_input=task_input,
                    version=version,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[
                self.instance
            ].client.TriggerOrganizationModelBinaryFileUpload,
            request=model_interface.TriggerOrganizationModelBinaryFileUploadRequest(
                name=f"{self.namespace}/models/{model_name}",
                # task_input=task_input,
                version=version,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

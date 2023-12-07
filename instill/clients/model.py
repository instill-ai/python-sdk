# pylint: disable=no-member,wrong-import-position
from typing import Dict

from google.protobuf import field_mask_pb2

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
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
        async_enabled: bool = False,
    ) -> model_interface.WatchUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.WatchUserModel,
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
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
    def create_model_local(
        self,
        model_name: str,
        model_description: str,
        model_path: str,
    ) -> model_interface.CreateUserModelBinaryFileUploadResponse:
        model = model_interface.Model()
        model.id = model_name
        model.description = model_description
        model.model_definition = "model-definitions/local"

        with open(model_path, "rb") as f:
            data = f.read()
            req = model_interface.CreateUserModelBinaryFileUploadRequest(
                parent=self.namespace, model=model, content=data
            )
        return RequestFactory(
            method=self.hosts[self.instance].client.CreateUserModelBinaryFileUpload,
            request=req,
            metadata=self.hosts[self.instance].metadata,
        ).send_stream()

    @grpc_handler
    def create_model(
        self,
        name: str,
        definition: str,
        configuration: dict,
        async_enabled: bool = False,
    ) -> model_interface.CreateUserModelResponse:
        model = model_interface.Model()
        model.id = name
        model.model_definition = definition
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
    def deploy_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.DeployUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeployUserModel,
                request=model_interface.DeployUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeployUserModel,
            request=model_interface.DeployUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def undeploy_model(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.UndeployUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UndeployUserModel,
                request=model_interface.UndeployUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UndeployUserModel,
            request=model_interface.UndeployUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def trigger_model(
        self,
        model_name: str,
        task_inputs: list,
        async_enabled: bool = False,
    ) -> model_interface.TriggerUserModelResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.TriggerUserModel,
                request=model_interface.TriggerUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}",
                    task_inputs=task_inputs,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.TriggerUserModel,
            request=model_interface.TriggerUserModelRequest(
                name=f"{self.namespace}/models/{model_name}", task_inputs=task_inputs
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
    def get_model_card(
        self,
        model_name: str,
        async_enabled: bool = False,
    ) -> model_interface.GetUserModelCardResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetUserModelCard,
                request=model_interface.GetUserModelCardRequest(
                    name=f"{self.namespace}/models/{model_name}"
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetUserModelCard,
            request=model_interface.GetUserModelCardRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_models(
        self,
        next_page_token: str = "",
        total_size: int = 100,
        show_deleted: bool = False,
        public=False,
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
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_operation(
        self,
        name: str,
        async_enabled: bool = False,
    ) -> model_interface.GetModelOperationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetModelOperation,
                request=model_interface.GetModelOperationRequest(
                    name=name,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetModelOperation,
            request=model_interface.GetModelOperationRequest(
                name=name,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

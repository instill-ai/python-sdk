# pylint: disable=no-member,wrong-import-position
import time
from typing import Dict, Iterable, Tuple, Union

from google.longrunning import operations_pb2
from google.protobuf import field_mask_pb2

# common
import instill.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck
import instill.protogen.model.model.v1alpha.model_definition_pb2 as model_definition_interface

# model
import instill.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
from instill.clients.base import Client
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

    def liveness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        resp: model_interface.LivenessResponse = self.hosts[
            self.instance
        ].client.Liveness(request=model_interface.LivenessRequest())
        return resp.health_check_response.status

    def readiness(self) -> healthcheck.HealthCheckResponse.ServingStatus:
        resp: model_interface.ReadinessResponse = self.hosts[
            self.instance
        ].client.Readiness(request=model_interface.ReadinessRequest())
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
    def watch_model(self, model_name: str) -> model_interface.Model.State.ValueType:
        resp: model_interface.WatchUserModelResponse = self.hosts[
            self.instance
        ].client.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.state

    @grpc_handler
    def create_model_local(
        self,
        model_name: str,
        model_description: str,
        model_path: str,
    ) -> model_interface.Model:
        model = model_interface.Model()
        model.id = model_name
        model.description = model_description
        model.model_definition = "model-definitions/local"

        with open(model_path, "rb") as f:
            data = f.read()
            req = model_interface.CreateUserModelBinaryFileUploadRequest(
                parent=self.namespace, model=model, content=data
            )
        create_resp: model_interface.CreateUserModelBinaryFileUploadResponse = (
            self.hosts[self.instance].client.CreateUserModelBinaryFileUpload(
                request_iterator=iter([req]),
                metadata=self.hosts[self.instance].metadata,
            )
        )

        while self.get_operation(name=create_resp.operation.name).done is not True:
            time.sleep(1)

        state = self.watch_model(model_name=model_name)
        while state == 0:
            time.sleep(1)
            state = self.watch_model(model_name=model_name)

        if state == 1:
            return self.get_model(model_name=model_name)

        raise SystemError("model creation failed")

    @grpc_handler
    def create_model(
        self,
        name: str,
        definition: str,
        configuration: dict,
    ) -> model_interface.Model:
        model = model_interface.Model()
        model.id = name
        model.model_definition = definition
        model.configuration.update(configuration)
        create_resp: model_interface.CreateUserModelResponse = self.hosts[
            self.instance
        ].client.CreateUserModel(
            request=model_interface.CreateUserModelRequest(
                model=model, parent=self.namespace
            ),
            metadata=self.hosts[self.instance].metadata,
        )

        while self.get_operation(name=create_resp.operation.name).done is not True:
            time.sleep(1)

        # TODO: due to state update delay of controller
        # TODO: should optimize this in model-backend
        time.sleep(3)

        state = self.watch_model(model_name=name)
        while state == 0:
            time.sleep(1)
            state = self.watch_model(model_name=name)

        if state == 1:
            return self.get_model(model_name=name)

        raise SystemError("model creation failed")

    @grpc_handler
    def deploy_model(self, model_name: str) -> model_interface.Model.State:
        self.hosts[self.instance].client.DeployUserModel(
            request=model_interface.DeployUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        )

        state = self.watch_model(model_name=model_name)
        while state not in (2, 3):
            time.sleep(1)
            state = self.watch_model(model_name=model_name)

        return state

    @grpc_handler
    def undeploy_model(self, model_name: str) -> model_interface.Model.State:
        self.hosts[self.instance].client.UndeployUserModel(
            request=model_interface.UndeployUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        )

        state = self.watch_model(model_name=model_name)
        while state not in (1, 3):
            time.sleep(1)
            state = self.watch_model(model_name=model_name)

        return state

    @grpc_handler
    def trigger_model(self, model_name: str, task_inputs: list) -> Iterable:
        resp: model_interface.TriggerUserModelResponse = self.hosts[
            self.instance
        ].client.TriggerUserModel(
            request=model_interface.TriggerUserModelRequest(
                name=f"{self.namespace}/models/{model_name}", task_inputs=task_inputs
            ),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.task_outputs

    @grpc_handler
    def delete_model(self, model_name: str):
        self.hosts[self.instance].client.DeleteUserModel(
            request=model_interface.DeleteUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        )

    @grpc_handler
    def get_model(self, model_name: str) -> model_interface.Model:
        resp: model_interface.GetUserModelResponse = self.hosts[
            self.instance
        ].client.GetUserModel(
            request=model_interface.GetUserModelRequest(
                name=f"{self.namespace}/models/{model_name}",
                view=model_definition_interface.VIEW_FULL,
            ),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.model

    @grpc_handler
    def update_model(
        self, model: model_interface.Model, mask: field_mask_pb2.FieldMask
    ) -> model_interface.Model:
        resp: model_interface.UpdateUserModelResponse = self.hosts[
            self.instance
        ].client.UpdateUserModel(
            request=model_interface.UpdateUserModelRequest(
                model=model,
                update_mask=mask,
            ),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.model

    @grpc_handler
    def lookup_model(self, model_uid: str) -> model_interface.Model:
        resp: model_interface.LookUpModelResponse = self.hosts[
            self.instance
        ].client.LookUpModel(
            request=model_interface.LookUpModelRequest(permalink=f"models/{model_uid}"),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.model

    @grpc_handler
    def get_model_card(self, model_name: str) -> model_interface.ModelCard:
        resp: model_interface.GetUserModelCardResponse = self.hosts[
            self.instance
        ].client.GetUserModel(
            request=model_interface.GetUserModelCardRequest(
                name=f"{self.namespace}/models/{model_name}"
            ),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.readme

    @grpc_handler
    def list_models(self, public=False) -> Tuple[Iterable, str, int]:
        resp: Union[
            model_interface.ListModelsResponse, model_interface.ListUserModelsResponse
        ]
        if not public:
            resp = self.hosts[self.instance].client.ListUserModels(
                request=model_interface.ListUserModelsRequest(parent=self.namespace),
                metadata=self.hosts[self.instance].metadata,
            )
        else:
            resp = self.hosts[self.instance].client.ListModels(
                request=model_interface.ListModelsRequest(),
                metadata=self.hosts[self.instance].metadata,
            )

        return resp.models, resp.next_page_token, resp.total_size

    @grpc_handler
    def get_operation(self, name: str) -> operations_pb2.Operation:
        resp: model_interface.GetModelOperationResponse = self.hosts[
            self.instance
        ].client.GetModelOperation(
            request=model_interface.GetModelOperationRequest(
                name=name,
            ),
            metadata=self.hosts[self.instance].metadata,
        )
        return resp.operation

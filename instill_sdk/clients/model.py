# pylint: disable=no-member,wrong-import-position
import time
from collections import defaultdict
from typing import Tuple

import grpc

import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# model
import instill_sdk.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill_sdk.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
from instill_sdk.clients.base import Client

# common
from instill_sdk.configuration import global_config
from instill_sdk.utils.error_handler import grpc_handler


class ModelClient(Client):
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
                self.hosts[instance]["client"] = model_service.ModelPublicServiceStub(
                    channel
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

    def liveness(self) -> model_interface.LivenessResponse:
        return self.hosts[self.instance]["client"].Liveness(
            request=model_interface.LivenessRequest()
        )

    def readiness(self) -> model_interface.ReadinessResponse:
        return self.hosts[self.instance]["client"].Readiness(
            request=model_interface.ReadinessRequest()
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
    def watch_model(self, model_name: str) -> model_interface.Model.State:
        return (
            self.hosts[self.instance]["client"]
            .WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                )
            )
            .state
        )

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
        resp = self.hosts[self.instance]["client"].CreateUserModelBinaryFileUpload(
            request_iterator=iter([req])
        )

        while (
            self.hosts[self.instance]["client"]
            .GetModelOperation(
                request=model_interface.GetModelOperationRequest(
                    name=resp.operation.name
                )
            )
            .operation.done
            is not True
        ):
            time.sleep(1)

        watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            )
        )
        while watch_resp.state == 0:
            time.sleep(1)
            watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                )
            )

        if watch_resp.state == 1:
            return (
                self.hosts[self.instance]["client"]
                .GetUserModel(
                    request=model_interface.GetUserModelRequest(name=model_name)
                )
                .model
            )

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
        resp = self.hosts[self.instance]["client"].CreateUserModel(
            request=model_interface.CreateUserModelRequest(
                model=model, parent=self.namespace
            )
        )

        while (
            self.hosts[self.instance]["client"]
            .GetModelOperation(
                request=model_interface.GetModelOperationRequest(
                    name=resp.operation.name
                )
            )
            .operation.done
            is not True
        ):
            time.sleep(1)

        # TODO: due to state update delay of controller
        # TODO: should optimize this in model-backend
        time.sleep(3)

        watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self.namespace}/models/{model.id}"
            )
        )
        while watch_resp.state == 0:
            time.sleep(1)
            watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model.id}"
                )
            )

        if watch_resp.state == 1:
            return (
                self.hosts[self.instance]["client"]
                .GetUserModel(
                    request=model_interface.GetUserModelRequest(
                        name=f"{self.namespace}/models/{model.id}"
                    )
                )
                .model
            )

        raise SystemError("model creation failed")

    @grpc_handler
    def deploy_model(self, model_name: str) -> model_interface.Model.State:
        self.hosts[self.instance]["client"].DeployUserModel(
            request=model_interface.DeployUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            )
        )

        watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            )
        )
        while watch_resp.state not in (2, 3):
            time.sleep(1)
            watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                )
            )

        return watch_resp.state

    @grpc_handler
    def undeploy_model(self, model_name: str) -> model_interface.Model.State:
        self.hosts[self.instance]["client"].UndeployUserModel(
            request=model_interface.UndeployUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            )
        )

        watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            )
        )
        while watch_resp.state not in (1, 3):
            time.sleep(1)
            watch_resp = self.hosts[self.instance]["client"].WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                )
            )

        return watch_resp.state

    @grpc_handler
    def trigger_model(self, model_name: str, task_inputs: list) -> list:
        resp = self.hosts[self.instance]["client"].TriggerUserModel(
            request=model_interface.TriggerUserModelRequest(
                name=f"{self.namespace}/models/{model_name}", task_inputs=task_inputs
            )
        )
        return resp.task_outputs

    @grpc_handler
    def delete_model(self, model_name: str):
        self.hosts[self.instance]["client"].DeleteUserModel(
            request=model_interface.DeleteUserModelRequest(
                name=f"{self.namespace}/models/{model_name}"
            )
        )

    @grpc_handler
    def get_model(self, model_name: str) -> model_interface.Model:
        return (
            self.hosts[self.instance]["client"]
            .GetUserModel(
                request=model_interface.GetUserModelRequest(
                    name=f"{self.namespace}/models/{model_name}"
                )
            )
            .model
        )

    @grpc_handler
    def get_model_by_uid(self, model_uid: str) -> model_interface.Model:
        return (
            self.hosts[self.instance]["client"]
            .GetUserModel(
                request=model_interface.LookUpModelRequest(
                    permalink=f"models/{model_uid}"
                )
            )
            .model
        )

    @grpc_handler
    def get_model_card(self, model_name: str) -> model_interface.Model:
        return (
            self.hosts[self.instance]["client"]
            .GetUserModel(
                request=model_interface.GetUserModelCardRequest(
                    name=f"{self.namespace}/models/{model_name}"
                )
            )
            .readme
        )

    @grpc_handler
    def list_models(self, public=False) -> Tuple[list, str, int]:
        if not public:
            resp = self.hosts[self.instance]["client"].ListUserModels(
                request=model_interface.ListUserModelsRequest(parent=self.namespace)
            )
        else:
            resp = self.hosts[self.instance]["client"].ListModels(
                request=model_interface.ListModelsRequest()
            )

        return resp.models, resp.next_page_token, resp.total_size

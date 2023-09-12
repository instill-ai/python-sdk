# pylint: disable=no-member,wrong-import-position
import time

import grpc

# mgmt
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface

# common
import instill_sdk.protogen.common.healthcheck.v1alpha.healthcheck_pb2 as healthcheck

# model
import instill_sdk.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill_sdk.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
from instill_sdk.clients.client import Client
from instill_sdk.utils.error_handler import grpc_handler


class ModelClient(Client):
    def __init__(
        self, user: mgmt_interface.User, token="", host="localhost", port="9080"
    ) -> None:
        """Initialize client for model service with target host.

        Args:
            token (str): api token for authentication
            host (str): host url
            port (str): host port
        """

        self.token = token
        self.host = host
        self.port = port

        self._user = user
        if len(token) == 0:
            self._channel = grpc.insecure_channel(f"{host}:{port}")
        else:
            ssl_creds = grpc.ssl_channel_credentials()
            call_creds = grpc.access_token_call_credentials(token)
            creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
            self._channel = grpc.secure_channel(
                target=f"{host}",
                credentials=creds,
            )
        self._stub = model_service.ModelPublicServiceStub(self._channel)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host: str):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port: str):
        self._port = port

    @grpc_handler
    def liveness(self) -> model_interface.LivenessResponse:
        return self._stub.Liveness(request=model_interface.LivenessRequest())

    @grpc_handler
    def readiness(self) -> model_interface.ReadinessResponse:
        return self._stub.Readiness(request=model_interface.ReadinessRequest())

    @grpc_handler
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
        return self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        ).state

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
                parent=self._user.name, model=model, content=data
            )
        resp = self._stub.CreateUserModelBinaryFileUpload(request_iterator=iter([req]))

        while (
            self._stub.GetModelOperation(
                request=model_interface.GetModelOperationRequest(
                    name=resp.operation.name
                )
            ).operation.done
            is not True
        ):
            time.sleep(1)

        watch_resp = self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )
        while watch_resp.state == 0:
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        if watch_resp.state == 1:
            return self._stub.GetUserModel(
                request=model_interface.GetUserModelRequest(name=model_name)
            ).model

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
        resp = self._stub.CreateUserModel(
            request=model_interface.CreateUserModelRequest(
                model=model, parent=self._user.name
            )
        )

        while (
            self._stub.GetModelOperation(
                request=model_interface.GetModelOperationRequest(
                    name=resp.operation.name
                )
            ).operation.done
            is not True
        ):
            time.sleep(1)

        watch_resp = self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model.id}"
            )
        )
        while watch_resp.state == 0:
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model.id}"
                )
            )

        if watch_resp.state == 1:
            return self._stub.GetUserModel(
                request=model_interface.GetUserModelRequest(
                    name=f"{self._user.name}/models/{model.id}"
                )
            ).model

        raise SystemError("model creation failed")

    @grpc_handler
    def deploy_model(self, model_name: str) -> model_interface.Model.State:
        self._stub.DeployUserModel(
            request=model_interface.DeployUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )

        watch_resp = self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )
        while watch_resp.state not in (2, 3):
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        return watch_resp.state

    @grpc_handler
    def undeploy_model(self, model_name: str) -> model_interface.Model.State:
        self._stub.UndeployUserModel(
            request=model_interface.UndeployUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )

        watch_resp = self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )
        while watch_resp.state not in (1, 3):
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        return watch_resp.state

    @grpc_handler
    def trigger_model(self, model_name: str, task_inputs: list) -> list:
        resp = self._stub.TriggerUserModel(
            request=model_interface.TriggerUserModelRequest(
                name=f"{self._user.name}/models/{model_name}", task_inputs=task_inputs
            )
        )
        return resp.task_outputs

    @grpc_handler
    def delete_model(self, model_name: str):
        self._stub.DeleteUserModel(
            request=model_interface.DeleteUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )

    @grpc_handler
    def get_model(self, model_name: str) -> model_interface.Model:
        return self._stub.GetUserModel(
            request=model_interface.GetUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        ).model

    @grpc_handler
    def list_models(self) -> list:
        models = []
        resp = self._stub.ListUserModels(
            request=model_interface.ListUserModelsRequest(parent=self._user.name)
        )
        models.extend(resp.models)
        while resp.next_page_token != "":
            resp = self._stub.ListUserModels(
                request=model_interface.ListUserModelsRequest(
                    parent=self._user.name,
                    page_token=resp.next_page_token,
                )
            )
            models.extend(resp.models)
        return models

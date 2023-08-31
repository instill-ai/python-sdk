# pylint: disable=no-member,wrong-import-position
import sys
import time
from abc import ABC, abstractmethod

import grpc

sys.path.insert(0, "./instill_sdk/protogen")

import instill_sdk.protogen.base.mgmt.v1alpha.metric_pb2 as metric_interface

# mgmt
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_pb2 as mgmt_interface
import instill_sdk.protogen.base.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service

# model
import instill_sdk.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill_sdk.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
from instill_sdk.utils.error_handler import grpc_handler
from instill_sdk.utils.logger import Logger

# connector
# import instill_sdk.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
# import instill_sdk.protogen.vdp.connector.v1alpha.connector_public_service_pb2_grpc as connector_service

# pipeline
# import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
# import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_public_service_pb2_grpc as pipeline_service


Logger.initialize()


class Client(ABC):
    """Base interface class for creating base/vdp/model clients.

    Args:
        ABC (abc.ABCMeta): std abstract class
    """

    @property
    @abstractmethod
    def protocol(self):
        pass

    @protocol.setter
    @abstractmethod
    def protocol(self):
        pass

    @property
    @abstractmethod
    def host(self):
        pass

    @host.setter
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def port(self):
        pass

    @port.setter
    @abstractmethod
    def port(self):
        pass

    @abstractmethod
    def liveness(self):
        raise NotImplementedError

    @abstractmethod
    def readiness(self):
        raise NotImplementedError

    @abstractmethod
    def is_serving(self):
        raise NotImplementedError


class MgmtClient(Client):
    def __init__(self, protocol="http", host="localhost", port="7080") -> None:
        """Initialize client for management service with target host.

        Args:
            protocol (str): http/https
            host (str): host url
            port (str): host port
        """

        self.protocol = protocol
        self.host = host
        self.port = port

        self._channel = grpc.insecure_channel(
            f"{host}:{port}".format(protocol=protocol, host=host, port=port)
        )
        self._stub = mgmt_service.MgmtPublicServiceStub(self._channel)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        self._protocol = protocol

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
    def liveness(self) -> mgmt_interface.LivenessResponse:
        return self._stub.Liveness(request=mgmt_interface.LivenessRequest())

    @grpc_handler
    def readiness(self) -> mgmt_interface.ReadinessResponse:
        return self._stub.Readiness(request=mgmt_interface.ReadinessRequest())

    @grpc_handler
    def is_serving(self) -> bool:
        try:
            return bool(self.readiness().health_check_response.status)
        except Exception:
            return False

    @grpc_handler
    def get_user(self) -> mgmt_interface.User:
        response = self._stub.QueryAuthenticatedUser(
            request=mgmt_interface.QueryAuthenticatedUserRequest()
        )
        return response.user

    @grpc_handler
    def list_pipeline_trigger_records(
        self,
    ) -> metric_interface.ListPipelineTriggerRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest()
        )

    @grpc_handler
    def list_pipeline_trigger_table_records(
        self,
    ) -> metric_interface.ListPipelineTriggerTableRecordsRequest:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerTableRecordsResponse()
        )

    @grpc_handler
    def list_pipeline_trigger_chart_records(
        self,
    ) -> metric_interface.ListPipelineTriggerChartRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListPipelineTriggerChartRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_records(
        self,
    ) -> metric_interface.ListConnectorExecuteRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_table_records(
        self,
    ) -> metric_interface.ListConnectorExecuteTableRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteTableRecordsRequest()
        )

    @grpc_handler
    def list_connector_execute_chart_records(
        self,
    ) -> metric_interface.ListConnectorExecuteChartRecordsResponse:
        return self._stub.ListPipelineTriggerRecords(
            request=metric_interface.ListConnectorExecuteChartRecordsRequest()
        )


class ModelClient(Client):
    def __init__(
        self, user: mgmt_interface.User, protocol="http", host="localhost", port="9080"
    ) -> None:
        """Initialize client for management service with target host.

        Args:
            protocol (str): http/https
            host (str): host url
            port (str): host port
        """

        self.protocol = protocol
        self.host = host
        self.port = port

        self._user = user
        self._channel = grpc.insecure_channel(
            f"{host}:{port}".format(protocol=protocol, host=host, port=port)
        )
        self._stub = model_service.ModelPublicServiceStub(self._channel)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        self._protocol = protocol

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
    def liveness(self) -> mgmt_interface.LivenessResponse:
        return self._stub.Liveness(request=mgmt_interface.LivenessRequest())

    @grpc_handler
    def readiness(self) -> mgmt_interface.ReadinessResponse:
        return self._stub.Readiness(request=mgmt_interface.ReadinessRequest())

    @grpc_handler
    def is_serving(self) -> bool:
        return bool(self.readiness().health_check_response.status)

    @grpc_handler
    def create_model_local(
        self, model_name: str, model_description: str, model_path: str
    ) -> bool:
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
            Logger.i(f"{model_name} creating...")
            time.sleep(1)

        watch_resp = self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )
        while watch_resp.state == 0:
            Logger.i(f"{model_name} creating...")
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        return watch_resp.state == 1

    @grpc_handler
    def create_github_model(
        self, model_name: str, model_repo: str, model_tag: str
    ) -> bool:
        model = model_interface.Model()
        model.id = model_name
        model.model_definition = "model-definitions/github"
        model.configuration.update(
            {
                "repository": model_repo,
                "tag": model_tag,
            },
        )

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
            Logger.i(f"{model_name} creating...")
            time.sleep(1)

        watch_resp = self._stub.WatchUserModel(
            request=model_interface.WatchUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )
        while watch_resp.state == 0:
            Logger.i(f"{model_name} creating...")
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        return watch_resp.state == 1

    @grpc_handler
    def deploy_model(self, model_name: str) -> bool:
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
            Logger.i(f"{model_name} deploying...")
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        return watch_resp.state == 2

    @grpc_handler
    def undeploy_model(self, model_name: str) -> bool:
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
            Logger.i(f"{model_name} undeploying...")
            time.sleep(1)
            watch_resp = self._stub.WatchUserModel(
                request=model_interface.WatchUserModelRequest(
                    name=f"{self._user.name}/models/{model_name}"
                )
            )

        return watch_resp.state == 1

    @grpc_handler
    def delete_model(self, model_name: str) -> bool:
        self._stub.DeleteUserModel(
            request=model_interface.DeleteUserModelRequest(
                name=f"{self._user.name}/models/{model_name}"
            )
        )

        return True

    @grpc_handler
    def list_models(self) -> model_interface.ListUserModelsResponse:
        return self._stub.ListUserModels(
            model_interface.ListUserModelsRequest(parent=self._user.name)
        )

# pylint: disable=no-member,wrong-import-position,no-name-in-module
import time

import instill.protogen.model.model.v1alpha.model_definition_pb2 as model_definition_interface
import instill.protogen.model.model.v1alpha.model_pb2 as model_interface
from instill.clients import InstillClient
from instill.resources.resource import Resource


class Model(Resource):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        definition: str,
        configuration: dict,
    ) -> None:
        super().__init__()
        self.client = client
        get_resp = client.model_service.get_model(model_name=name, silent=True)
        if get_resp is None:
            operation = client.model_service.create_model(
                name=name,
                definition=definition,
                configuration=configuration,
            ).operation
            while (
                client.model_service.get_operation(name=operation.name).operation.done
                is not True
            ):
                time.sleep(1)
            # TODO: due to state update delay of controller
            # TODO: should optimize this in model-backend
            time.sleep(3)

            state = client.model_service.watch_model(model_name=name).state
            while state == 0:
                time.sleep(1)
                state = client.model_service.watch_model(model_name=name).state

            if state == 1:
                model = client.model_service.get_model(model_name=name).model
            else:
                raise BaseException("model creation failed")
        else:
            model = get_resp.model

        self.resource = model

    def __call__(self, task_inputs: list) -> list:
        return self.client.model_service.trigger_model(
            self.resource.id, task_inputs
        ).task_outputs

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: InstillClient):
        self._client = client

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource: model_interface.Model):
        self._resource = resource

    def _update(self):
        self.resource = self.client.model_service.get_model(
            model_name=self.resource.id
        ).model

    def get_definition(self) -> model_definition_interface.ModelDefinition:
        return self.resource.model_definition

    def get_readme(self) -> str:
        return self.client.model_service.get_model_card(self.resource.id).readme

    def get_state(self) -> model_interface.Model.State:
        return self.client.model_service.watch_model(self.resource.id).state

    def deploy(self) -> model_interface.Model.State:
        self.client.model_service.deploy_model(self.resource.id)
        state = self.client.model_service.watch_model(model_name=self.resource.id).state
        while state not in (2, 3):
            time.sleep(1)
            state = self.client.model_service.watch_model(
                model_name=self.resource.id
            ).state
        self._update()
        return state

    def undeploy(self) -> model_interface.Model.State:
        self.client.model_service.undeploy_model(self.resource.id)
        state = self.client.model_service.watch_model(model_name=self.resource.id).state
        while state not in (1, 3):
            time.sleep(1)
            state = self.client.model_service.watch_model(
                model_name=self.resource.id
            ).state
        self._update()
        return state

    def delete(self):
        if self.resource is not None:
            self.client.model_service.delete_model(self.resource.id)


class GithubModel(Model):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        model_repo: str,
        model_tag: str,
    ) -> None:
        definition = "model-definitions/github"
        configuration = {"repository": model_repo, "tag": model_tag}
        super().__init__(
            client=client,
            name=name,
            definition=definition,
            configuration=configuration,
        )


class HugginfaceModel(Model):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        model_repo: str,
    ) -> None:
        configuration = {"repo_id": model_repo}
        definition = "model-definitions/huggingface"
        super().__init__(
            client=client,
            name=name,
            definition=definition,
            configuration=configuration,
        )

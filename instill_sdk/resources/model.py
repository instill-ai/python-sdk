# pylint: disable=no-member,wrong-import-position
import instill_sdk.protogen.model.model.v1alpha.model_pb2 as model_interface
from instill_sdk.clients.model import ModelClient
from instill_sdk.resources.resource import Resource


class Model(Resource):
    def __init__(
        self,
        client: ModelClient,
        name: str,
        definition: str,
        configuration: dict,
    ) -> None:
        super().__init__()
        self.client = client
        model = client.create_model(
            name=name,
            definition=definition,
            configuration=configuration,
        )
        if model is None:
            model = client.get_model(model_name=name)
            if model is None:
                raise BaseException("model creation failed")

        self.resource = model

    def __del__(self):
        if self.resource is not None:
            self.client.delete_model(self.resource.id)

    def __call__(self, task_inputs: list) -> list:
        return self.client.trigger_model(self.resource.id, task_inputs)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: ModelClient):
        self._client = client

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource: model_interface.Model):
        self._resource = resource

    def _update(self):
        self.resource = self.client.get_model(model_name=self.resource.id)

    def get_definition(self) -> str:
        return self.resource.model_definition

    def get_state(self) -> model_interface.Model.State:
        return self.client.watch_model(self.resource.id)

    def deploy(self) -> model_interface.Model:
        self.client.deploy_model(self.resource.id)
        self._update()
        return self._resource

    def undeploy(self) -> model_interface.Model:
        self.client.undeploy_model(self.resource.id)
        self._update()
        return self._resource


class GithubModel(Model):
    def __init__(
        self,
        client: ModelClient,
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
        client: ModelClient,
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
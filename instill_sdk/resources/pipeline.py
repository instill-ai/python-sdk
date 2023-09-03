# pylint: disable=no-member,wrong-import-position
import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
from instill_sdk.clients.pipeline import PipelineClient
from instill_sdk.resources.resource import Resource


class Pipeline(Resource):
    def __init__(
        self,
        client: PipelineClient,
        name: str,
        recipe: pipeline_interface.Recipe,
    ) -> None:
        super().__init__()
        self.client = client
        pipeline = client.create_pipeline(name=name, recipe=recipe)
        if pipeline is None:
            pipeline = client.get_pipeline(name=name)
            if pipeline is None:
                raise BaseException("model creation failed")

        self.resource = pipeline

    def __del__(self):
        if self.resource is not None:
            self.client.delete_pipeline(self.resource.id)

    def __call__(self, task_inputs: list) -> list:
        return self.client.trigger_pipeline(self.resource.id, task_inputs)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: PipelineClient):
        self._client = client

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource: pipeline_interface.Pipeline):
        self._resource = resource

    def _update(self):
        self.resource = self.client.get_pipeline(name=self.resource.id)

    def get_recipe(self) -> str:
        return self.resource.recipe

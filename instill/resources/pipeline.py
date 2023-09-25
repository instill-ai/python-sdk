# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Tuple

import instill.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
from instill.clients import InstillClient
from instill.resources.resource import Resource


class Pipeline(Resource):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        recipe: pipeline_interface.Recipe,
    ) -> None:
        super().__init__()
        self.client = client
        pipeline = client.pipeline_service.get_pipeline(name=name, silent=True)
        if pipeline is None:
            pipeline = client.pipeline_service.create_pipeline(name=name, recipe=recipe)
            if pipeline is None:
                raise BaseException("pipeline creation failed")

        self.resource = pipeline

    def __del__(self):
        if self.resource is not None:
            self.client.pipeline_service.delete_pipeline(self.resource.id)

    def __call__(
        self, task_inputs: list
    ) -> Tuple[list, pipeline_interface.TriggerMetadata]:
        return self.client.pipeline_service.trigger_pipeline(
            self.resource.id, task_inputs
        )

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
    def resource(self, resource: pipeline_interface.Pipeline):
        self._resource = resource

    def _update(self):
        self.resource = self.client.pipeline_service.get_pipeline(name=self.resource.id)

    def get_recipe(self) -> str:
        return self.resource.recipe

    def validate_pipeline(self) -> pipeline_interface.Pipeline:
        return self.client.pipeline_service.validate_pipeline(name=self.resource.id)

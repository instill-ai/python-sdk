# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Tuple, Union

import grpc
from google.longrunning import operations_pb2
from google.protobuf.field_mask_pb2 import FieldMask

import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
from instill.clients import InstillClient
from instill.resources.resource import Resource
from instill.utils.logger import Logger


class Pipeline(Resource):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        recipe: Union[pipeline_interface.Recipe, None] = None,
    ) -> None:
        super().__init__()
        self.client = client
        get_resp = client.pipeline_service.get_pipeline(name=name, silent=True)
        if get_resp is None:
            pipeline = client.pipeline_service.create_pipeline(
                name=name, recipe=recipe
            ).pipeline
            if pipeline is None:
                raise BaseException("pipeline creation failed")
        else:
            pipeline = get_resp.pipeline

        self.resource = pipeline

    def __call__(
        self, task_inputs: list
    ) -> Tuple[list, pipeline_interface.TriggerMetadata]:
        resp = self.client.pipeline_service.trigger_pipeline(
            self.resource.id, task_inputs
        )
        return resp.outputs, resp.metadata

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

    def get_operation(self, operation: operations_pb2.Operation):
        return self.client.pipeline_service.get_operation(operation.name).operation

    def trigger_async(self, task_inputs: list) -> operations_pb2.Operation:
        return self.client.pipeline_service.trigger_async_pipeline(
            self.resource.id, task_inputs
        ).operation

    def get_recipe(self) -> pipeline_interface.Recipe:
        return self.resource.recipe

    def update_recipe(self, recipe: pipeline_interface.Recipe):
        pipeline = self.resource
        pipeline.recipe.CopyFrom(recipe)
        self.client.pipeline_service.update_pipeline(
            pipeline, FieldMask(paths=["recipe"])
        )
        self._update()

    def validate_pipeline(self) -> bool:
        try:
            self.client.pipeline_service.validate_pipeline(
                name=self.resource.id, silent=True
            )
            return True
        except grpc.RpcError as rpc_error:
            Logger.w(rpc_error.code())
            Logger.w(rpc_error.details())
            return False

    def delete(self):
        if self.resource is not None:
            self.client.pipeline_service.delete_pipeline(self.resource.id)

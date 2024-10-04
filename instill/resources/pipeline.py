# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Optional, Tuple, Union

import grpc
from google.longrunning.operations_pb2 import Operation
from google.protobuf import json_format
from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.struct_pb2 import Struct

import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
from instill.clients import InstillClient
from instill.resources.resource import Resource
from instill.utils.logger import Logger


class Pipeline(Resource):
    def __init__(
        self,
        client: InstillClient,
        namespace_id: str,
        pipeline_id: str,
        recipe: Union[Struct, None] = None,
    ) -> None:
        super().__init__()
        self.client = client
        get_resp = None
        pipeline = None
        get_resp = client.pipeline.get_pipeline(
            namespace_id=namespace_id,
            pipeline_id=pipeline_id,
        )
        if get_resp is None:
            pipeline = client.pipeline.create_pipeline(
                namespace_id=namespace_id,
                recipe=recipe,
            ).pipeline
            if pipeline is None:
                raise BaseException("pipeline creation failed")
        else:
            pipeline = get_resp.pipeline

        self.resource = pipeline

    def __call__(
        self,
        task_inputs: list,
        silent: bool = False,
    ) -> Optional[Tuple[list, pipeline_interface.TriggerMetadata]]:
        resp = self.client.pipeline.trigger(
            self.resource.id,
            task_inputs,
            silent=silent,
        )
        if resp is not None:
            return resp.outputs, resp.metadata
        return resp

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
        self.resource = self.client.pipeline.get_pipeline(name=self.resource.id)

    def get_operation(self, operation: Operation, silent: bool = False):
        response = self.client.pipeline.get_operation(
            operation.name,
            silent=silent,
        )
        if response is not None:
            return response.operation
        return response

    def trigger_async(
        self,
        task_inputs: list,
        silent: bool = False,
    ) -> Operation:
        response = self.client.pipeline.trigger_async(
            self.resource.id,
            task_inputs,
            silent=silent,
        )
        if response is not None:
            return response.operation
        return response

    def get_recipe(self) -> dict:
        return json_format.MessageToDict(self.resource.recipe)

    def update_recipe(self, recipe: Struct, silent: bool = False):
        pipeline = self.resource
        pipeline.recipe.CopyFrom(recipe)
        self.client.pipeline.update_pipeline(
            pipeline,
            FieldMask(paths=["recipe"]),
            silent=silent,
        )
        self._update()

    def validate_pipeline(self, silent: bool = True) -> bool:
        try:
            self.client.pipeline.validate_pipeline(name=self.resource.id, silent=silent)
            return True
        except grpc.RpcError as rpc_error:
            Logger.w(rpc_error.code())
            Logger.w(rpc_error.details())
            return False

    def delete(self, silent: bool = False):
        if self.resource is not None:
            self.client.pipeline.delete_pipeline(self.resource.id, silent=silent)

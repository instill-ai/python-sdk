# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Optional, Tuple, Union

import grpc
from google.longrunning import operations_pb2
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
        name: str,
        recipe: Union[Struct, None] = None,
    ) -> None:
        super().__init__()
        self.client = client
        get_resp = None
        pipeline = None
        if client.pipeline_service.target_namespace.startswith("users"):
            get_resp = client.pipeline_service.get_pipeline(name=name, silent=True)
            if get_resp is None:
                pipeline = client.pipeline_service.create_pipeline(
                    name=name, recipe=recipe
                ).pipeline
                if pipeline is None:
                    raise BaseException("pipeline creation failed")
            else:
                pipeline = get_resp.pipeline
        elif client.pipeline_service.target_namespace.startswith("organizations"):
            get_resp = client.pipeline_service.get_org_pipeline(name=name, silent=True)
            if get_resp is None:
                pipeline = client.pipeline_service.create_org_pipeline(
                    name=name, recipe=recipe
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
        resp = self.client.pipeline_service.trigger_pipeline(
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
        self.resource = self.client.pipeline_service.get_pipeline(name=self.resource.id)

    def get_operation(self, operation: operations_pb2.Operation, silent: bool = False):
        response = self.client.pipeline_service.get_operation(
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
    ) -> operations_pb2.Operation:
        response = self.client.pipeline_service.trigger_async_pipeline(
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
        self.client.pipeline_service.update_pipeline(
            pipeline,
            FieldMask(paths=["recipe"]),
            silent=silent,
        )
        self._update()

    def validate_pipeline(self, silent: bool = True) -> bool:
        try:
            self.client.pipeline_service.validate_pipeline(
                name=self.resource.id, silent=silent
            )
            return True
        except grpc.RpcError as rpc_error:
            Logger.w(rpc_error.code())
            Logger.w(rpc_error.details())
            return False

    def delete(self, silent: bool = False):
        if self.resource is not None:
            self.client.pipeline_service.delete_pipeline(
                self.resource.id, silent=silent
            )

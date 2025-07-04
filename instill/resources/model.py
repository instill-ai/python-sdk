"""Model resource module."""

# pylint: disable=no-member

from typing import Optional

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
        get_resp = client.model.get_model(model_name=name, silent=True)
        if get_resp is None:
            model = client.model.create_model(
                name=name,
                definition=definition,
                configuration=configuration,
            ).model
            if model is None:
                raise BaseException("model creation failed")
        else:
            model = get_resp.model

        self.resource = model

    def __call__(self, task_inputs: list, silent: bool = False) -> Optional[list]:
        response = self.client.model.trigger(
            self.resource.id,
            task_inputs,
            silent=silent,
        )
        if response is not None:
            return response.task_outputs
        return response

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
    def resource(
        self, resource: Optional[model_interface.Model]
    ):  # pylint: disable=no-member
        self._resource = resource

    def _update(self):
        self.resource = self.client.model.get_model(model_name=self.resource.id).model

    def get_definition(
        self,
    ) -> model_definition_interface.ModelDefinition:  # pylint: disable=no-member
        return self.resource.model_definition

    def delete(self, silent: bool = False):
        if self.resource is not None:
            self.client.model.delete_model(
                self.resource.id,
                silent=silent,
            )

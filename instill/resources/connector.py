# pylint: disable=no-member,wrong-import-position,no-name-in-module
import instill.protogen.vdp.pipeline.v1beta.connector_definition_pb2 as connector_definition_interface
import instill.protogen.vdp.pipeline.v1beta.connector_pb2 as connector_interface
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
from instill.clients import InstillClient
from instill.resources.resource import Resource


class Connector(Resource):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        definition: str,
        configuration: dict,
    ) -> None:
        super().__init__()
        self.client = client
        get_resp = client.pipeline_service.get_connector(name=name, silent=True)
        if get_resp is None:
            connector = client.pipeline_service.create_connector(
                name=name,
                definition=definition,
                configuration=configuration,
            ).connector
            if connector is None:
                raise BaseException("connector creation failed")
        else:
            connector = get_resp.connector

        self.resource = connector

    def __call__(self, task_inputs: list, mode="execute"):
        if mode == "execute":
            resp = self.client.pipeline_service.execute_connector(
                self.resource.id, task_inputs
            )
            return resp.outputs
        return self.test()

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
    def resource(self, resource: connector_interface.Connector):
        self._resource = resource

    def _create_component(
        self,
        name: str,
        config: dict,
    ) -> pipeline_interface.Component:
        component = pipeline_interface.Component()
        component.id = name
        component.definition_name = self.get_definition().name
        component.resource_name = self.resource.name
        component.configuration.update(config)
        return component

    def get_definition(self) -> connector_definition_interface.ConnectorDefinition:
        return self.resource.connector_definition

    def get_state(self) -> connector_interface.Connector.State:
        return self.client.pipeline_service.watch_connector(self.resource.id).state

    def test(self) -> connector_interface.Connector.State:
        return self.client.pipeline_service.test_connector(self.resource.id).state

    def delete(self):
        if self.resource is not None:
            self.client.pipeline_service.delete_connector(self.resource.id)

# pylint: disable=no-member,wrong-import-position
import instill_sdk.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
from instill_sdk.clients.connector import ConnectorClient
from instill_sdk.resources.resource import Resource


class Connector(Resource):
    def __init__(
        self,
        client: ConnectorClient,
        name: str,
        definition: str,
        configuration: dict,
    ) -> None:
        super().__init__()
        self.client = client
        connector = client.create_connector(
            name=name,
            definition=definition,
            configuration=configuration,
        )
        if connector is None:
            connector = client.get_connector(name=name)
            if connector is None:
                raise BaseException("connector creation failed")

        self.resource = connector
        self._is_connect = False

    def __del__(self):
        if self.resource is not None:
            self.client.delete_connector(self.resource.id)

    def __call__(self, task_inputs: list, mode="execute") -> list:
        if not self._is_connect:
            raise BaseException("test and connect the connector first")
        if mode == "execute":
            return self.client.execute_connector(self.resource.id, task_inputs)
        return self.client.test_connector(self.resource.id, task_inputs)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: ConnectorClient):
        self._client = client

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource: connector_interface.ConnectorResource):
        self._resource = resource

    def get_definition(self) -> str:
        return self.resource.connector_definition

    def get_state(self) -> connector_interface.ConnectorResource.State:
        return self.client.watch_connector(self.resource.id)

    def test(self) -> connector_interface.ConnectorResource.State:
        state = self.client.test_connector(self.resource.id)
        if state == connector_interface.ConnectorResource.STATE_CONNECTED:
            self._is_connect = True
        else:
            self._is_connect = False

        return state

    def connect(self):
        connector = self.client.connect_connector(self.resource.id)
        self._is_connect = (
            connector.state == connector_interface.ConnectorResource.STATE_CONNECTED
        )

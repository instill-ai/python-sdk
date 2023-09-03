# pylint: disable=no-member,wrong-import-position
from instill_sdk.clients.connector import ConnectorClient
from instill_sdk.resources.connector import Connector


class PineconeConnector(Connector):
    def __init__(
        self,
        client: ConnectorClient,
        name: str,
        api_key: str,
        server_url: str,
    ) -> None:
        definition = "connector-definitions/data-pinecone"
        configuration = {"url": server_url, "api_key": api_key}
        super().__init__(client, name, definition, configuration)

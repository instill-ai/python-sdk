# pylint: disable=no-member,wrong-import-position,no-name-in-module
from instill.clients import InstillClient
from instill.resources.connector import Connector


class PineconeConnector(Connector):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        api_key: str,
        server_url: str,
    ) -> None:
        definition = "connector-definitions/pinecone"
        configuration = {"url": server_url, "api_key": api_key}
        super().__init__(client, name, definition, configuration)

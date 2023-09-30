# pylint: disable=no-member,wrong-import-position,no-name-in-module
from instill.clients import InstillClient
from instill.resources.connector import Connector


class InstillModelConnector(Connector):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        server_url: str,
    ) -> None:
        definition = "connector-definitions/ai-instill-model"
        configuration = {
            "api_token": client.connector_service.hosts[
                client.connector_service.instance
            ]["token"],
            "server_url": server_url,
        }
        super().__init__(client, name, definition, configuration)


class StabilityAIConnector(Connector):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        api_key: str,
    ) -> None:
        definition = "connector-definitions/ai-stability-ai"
        configuration = {"api_key": api_key}
        super().__init__(client, name, definition, configuration)


class OpenAIConnector(Connector):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        api_key: str,
    ) -> None:
        definition = "connector-definitions/ai-openai"
        configuration = {
            "api_key": api_key,
        }
        super().__init__(client, name, definition, configuration)

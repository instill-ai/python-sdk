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
        task: str,
        engine: str,
    ) -> None:
        definition = "connector-definitions/ai-stability-ai"
        configuration = {
            "api_key": api_key,
            "task": task,
            "engine": engine,
        }
        super().__init__(client, name, definition, configuration)


class OpenAIConnector(Connector):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        api_key: str,
        task: str,
        model_name: str,
        system_message: str,
        temperature: int,
    ) -> None:
        definition = "connector-definitions/ai-openai"
        configuration = {
            "api_key": api_key,
            "task": task,
            "model": model_name,
            "system_message": system_message,
            "temperature": temperature,
            "n": 1,
        }
        super().__init__(client, name, definition, configuration)

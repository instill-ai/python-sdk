# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json

import jsonschema

from instill.clients import InstillClient
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema.huggingface import HuggingFaceConnectorSpec
from instill.resources.schema.instill import (
    InstillModelConnector as InstillModelConnectorConfig,
)
from instill.resources.schema.openai import OpenAIConnectorResource
from instill.resources.schema.stabilityai import StabilityAIConnectorResource


class HuggingfaceConnector(Connector):
    """Huggingface Connector"""

    with open(
        f"{const.SPEC_PATH}/huggingface_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: HuggingFaceConnectorSpec,
    ) -> None:
        definition = "connector-definitions/hugging-face"

        jsonschema.validate(vars(config), StabilityAIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class InstillModelConnector(Connector):
    """Instill Model Connector"""

    with open(f"{const.SPEC_PATH}/instill_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        config: InstillModelConnectorConfig,
        name: str = "model-connector",
    ) -> None:
        definition = "connector-definitions/instill-model"

        if config.api_token == "":  # type: ignore
            config.api_token = client.model_service.hosts[  # type: ignore
                client.model_service.instance
            ].token
        if config.server_url == "":  # type: ignore
            config.server_url = "http://api-gateway:8080"  # type: ignore

        jsonschema.validate(vars(config), InstillModelConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class StabilityAIConnector(Connector):
    """Stability AI Connector"""

    with open(
        f"{const.SPEC_PATH}/stabilityai_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: StabilityAIConnectorResource,
    ) -> None:
        definition = "connector-definitions/stability-ai"

        jsonschema.validate(vars(config), StabilityAIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class OpenAIConnector(Connector):
    """OpenAI Connector"""

    with open(f"{const.SPEC_PATH}/openai_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: OpenAIConnectorResource,
    ) -> None:
        definition = "connector-definitions/openai"

        jsonschema.validate(vars(config), OpenAIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))

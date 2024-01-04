# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json

import jsonschema

from instill.clients import InstillClient
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema.numbers import NumbersProtocolBlockchainConnectorSpec


class NumbersConnector(Connector):
    """Numbers Connector"""

    with open(f"{const.SPEC_PATH}/numbers_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: NumbersProtocolBlockchainConnectorSpec,
    ) -> None:
        definition = "connector-definitions/numbers"

        jsonschema.validate(vars(config), NumbersConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))

# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json

import jsonschema

from instill.clients import InstillClient
from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import Component
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema import helper, numbers, numbers_task_commit_input


class NumbersConnector(Connector):
    """Numbers Connector"""

    with open(f"{const.SPEC_PATH}/numbers_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: numbers.NumbersProtocolBlockchainConnectorSpec,
    ) -> None:
        definition = "connector-definitions/numbers"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, NumbersConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: numbers_task_commit_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)

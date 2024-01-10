# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json

import jsonschema

from instill.clients import InstillClient
from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import Component
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema import (
    airbyte,
    airbyte_task_write_destination_input,
    helper,
)


class AirbyteAmazonsqsConnector(Connector):
    """Airbyte Amazonsqs Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Amazonsqs,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteAmazonsqsConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteAwsdatalakeConnector(Connector):
    """Airbyte Awsdatalake Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Awsdatalake,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteAwsdatalakeConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteAzureblobstorageConnector(Connector):
    """Airbyte Azureblobstorage Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Azureblobstorage,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(
            config, AirbyteAzureblobstorageConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteBigqueryConnector(Connector):
    """Airbyte Bigquery Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Bigquery,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteBigqueryConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteCassandraConnector(Connector):
    """Airbyte Cassandra Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Cassandra,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteCassandraConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteChromaConnector(Connector):
    """Airbyte Chroma Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Chroma,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteChromaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteClickhouseConnector(Connector):
    """Airbyte Clickhouse Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Clickhouse,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteClickhouseConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteConvexConnector(Connector):
    """Airbyte Convex Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Convex,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteConvexConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteCsvConnector(Connector):
    """Airbyte Csv Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Csv,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteCsvConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteCumulioConnector(Connector):
    """Airbyte Cumulio Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Cumulio,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteCumulioConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteDatabendConnector(Connector):
    """Airbyte Databend Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Databend,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteDatabendConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteDatabricksConnector(Connector):
    """Airbyte Databricks Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Databricks,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteDatabricksConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteDorisConnector(Connector):
    """Airbyte Doris Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Doris,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteDorisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteDuckdbConnector(Connector):
    """Airbyte Duckdb Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Duckdb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteDuckdbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteDynamodbConnector(Connector):
    """Airbyte Dynamodb Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Dynamodb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteDynamodbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteE2etestConnector(Connector):
    """Airbyte E2etest Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.E2etest,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteE2etestConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteElasticsearchConnector(Connector):
    """Airbyte Elasticsearch Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Elasticsearch,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(
            config, AirbyteElasticsearchConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteExasolConnector(Connector):
    """Airbyte Exasol Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Exasol,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteExasolConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteFireboltConnector(Connector):
    """Airbyte Firebolt Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Firebolt,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteFireboltConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteFirestoreConnector(Connector):
    """Airbyte Firestore Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Firestore,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteFirestoreConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteGcsConnector(Connector):
    """Airbyte Gcs Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Gcs,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteGcsConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteGooglesheetsConnector(Connector):
    """Airbyte Googlesheets Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Googlesheets,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteGooglesheetsConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteIcebergConnector(Connector):
    """Airbyte Iceberg Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Iceberg,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteIcebergConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteKafkaConnector(Connector):
    """Airbyte Kafka Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Kafka,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteKafkaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteKeenConnector(Connector):
    """Airbyte Keen Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Keen,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteKeenConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteKinesisConnector(Connector):
    """Airbyte Kinesis Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Kinesis,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteKinesisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteLangchainConnector(Connector):
    """Airbyte Langchain Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Langchain,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteLangchainConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteLocaljsonConnector(Connector):
    """Airbyte Localjson Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Localjson,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteLocaljsonConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteMariadbcolumnstoreConnector(Connector):
    """Airbyte Mariadbcolumnstore Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Mariadbcolumnstore,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(
            config, AirbyteMariadbcolumnstoreConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteMeilisearchConnector(Connector):
    """Airbyte Meilisearch Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Meilisearch,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteMeilisearchConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteMilvusConnector(Connector):
    """Airbyte Milvus Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Milvus,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteMilvusConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteMongodbConnector(Connector):
    """Airbyte Mongodb Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Mongodb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteMongodbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteMqttConnector(Connector):
    """Airbyte Mqtt Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Mqtt,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteMqttConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbytMssqlConnector(Connector):
    """Airbyte Mssql Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Mssql,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbytMssqlConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteMysqlConnector(Connector):
    """Airbyte Mysql Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Mysql,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteMysqlConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteOracleConnector(Connector):
    """Airbyte Oracle Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Oracle,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteOracleConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbytePineconeConnector(Connector):
    """Airbyte Pinecone Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Pinecone,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbytePineconeConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbytePostgresConnector(Connector):
    """Airbyte Postgres Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Postgres,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbytePostgresConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbytePubsubConnector(Connector):
    """Airbyte Pubsub Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Pubsub,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbytePubsubConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbytePulsarConnector(Connector):
    """Airbyte Pulsar Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Pulsar,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbytePulsarConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteQdrantConnector(Connector):
    """Airbyte Qdrant Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Qdrant,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteQdrantConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteR2Connector(Connector):
    """Airbyte R2 Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.R2,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteR2Connector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteRabbitmqConnector(Connector):
    """Airbyte Rabbitmq Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Rabbitmq,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteRabbitmqConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteRedisConnector(Connector):
    """Airbyte Redis Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Redis,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteRedisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteRedpandaConnector(Connector):
    """Airbyte Redpanda Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Redpanda,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteRedpandaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteRedshiftConnector(Connector):
    """Airbyte Redshift Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Redshift,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteRedshiftConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteRocksetConnector(Connector):
    """Airbyte Rockset Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Rockset,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteRocksetConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteS3glueConnector(Connector):
    """Airbyte S3glue Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.S3glue,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteS3glueConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteS3Connector(Connector):
    """Airbyte S3 Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.S3,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteS3Connector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteScyllaConnector(Connector):
    """Airbyte Scylla Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Scylla,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteScyllaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteSelectdbConnector(Connector):
    """Airbyte Selectdb Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Selectdb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteSelectdbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteSftpjsonConnector(Connector):
    """Airbyte Sftpjson Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Sftpjson,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteSftpjsonConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteSnowflakeConnector(Connector):
    """Airbyte Snowflake Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Snowflake,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteSnowflakeConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteSqliteConnector(Connector):
    """Airbyte Sqlite Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Sqlite,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteSqliteConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteStarburstgalaxyConnector(Connector):
    """Airbyte Starburstgalaxy Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Starburstgalaxy,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(
            config, AirbyteStarburstgalaxyConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteTeradataConnector(Connector):
    """Airbyte Teradata Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Teradata,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteTeradataConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteTidbConnector(Connector):
    """Airbyte Tidb Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Tidb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteTidbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteTimeplusConnector(Connector):
    """Airbyte Timeplus Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Timeplus,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteTimeplusConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteTypesenseConnector(Connector):
    """Airbyte Typesense Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Typesense,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteTypesenseConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteVerticaConnector(Connector):
    """Airbyte Vertica Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Vertica,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteVerticaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteWeaviateConnector(Connector):
    """Airbyte Weaviate Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Weaviate,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteWeaviateConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteXataConnector(Connector):
    """Airbyte Xata Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Xata,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteXataConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteYugabytedbConnector(Connector):
    """Airbyte Yugabytedb Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Yugabytedb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(config, AirbyteYugabytedbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class AirbyteAirbytedevmatecloudConnector(Connector):
    """Airbyte Airbytedevmatecloud Connector"""

    with open(f"{const.SPEC_PATH}/airbyte_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config_spec: airbyte.Airbytedevmatecloud,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config = helper.pop_default_and_to_dict(config_spec)
        jsonschema.validate(
            config, AirbyteAirbytedevmatecloudConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)

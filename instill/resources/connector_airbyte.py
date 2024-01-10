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
        config: airbyte.Amazonsqs,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteAmazonsqsConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Awsdatalake,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteAwsdatalakeConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Azureblobstorage,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config, AirbyteAzureblobstorageConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Bigquery,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteBigqueryConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Cassandra,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteCassandraConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Chroma,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteChromaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Clickhouse,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteClickhouseConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Convex,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteConvexConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Csv,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteCsvConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Cumulio,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteCumulioConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Databend,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteDatabendConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Databricks,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteDatabricksConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Doris,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteDorisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Duckdb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteDuckdbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Dynamodb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteDynamodbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.E2etest,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteE2etestConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Elasticsearch,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config, AirbyteElasticsearchConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Exasol,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteExasolConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Firebolt,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteFireboltConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Firestore,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteFirestoreConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Gcs,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteGcsConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Googlesheets,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteGooglesheetsConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Iceberg,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteIcebergConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Kafka,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteKafkaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Keen,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteKeenConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Kinesis,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteKinesisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Langchain,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteLangchainConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Localjson,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteLocaljsonConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Mariadbcolumnstore,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config, AirbyteMariadbcolumnstoreConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Meilisearch,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteMeilisearchConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Milvus,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteMilvusConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Mongodb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteMongodbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Mqtt,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteMqttConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Mssql,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbytMssqlConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Mysql,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteMysqlConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Oracle,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteOracleConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Pinecone,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbytePineconeConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Postgres,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbytePostgresConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Pubsub,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbytePubsubConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Pulsar,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbytePulsarConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Qdrant,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteQdrantConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.R2,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteR2Connector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Rabbitmq,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteRabbitmqConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Redis,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteRedisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Redpanda,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteRedpandaConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Redshift,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteRedshiftConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Rockset,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteRocksetConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.S3glue,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteS3glueConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.S3,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteS3Connector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Scylla,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteScyllaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Selectdb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteSelectdbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Sftpjson,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteSftpjsonConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Snowflake,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteSnowflakeConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Sqlite,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteSqliteConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Starburstgalaxy,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config, AirbyteStarburstgalaxyConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Teradata,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteTeradataConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Tidb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteTidbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Timeplus,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteTimeplusConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Typesense,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteTypesenseConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Vertica,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteVerticaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Weaviate,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteWeaviateConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Xata,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, AirbyteXataConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Yugabytedb,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, AirbyteYugabytedbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

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
        config: airbyte.Airbytedevmatecloud,
    ) -> None:
        definition = "connector-definitions/airbyte-destination"

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config, AirbyteAirbytedevmatecloudConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: airbyte_task_write_destination_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)

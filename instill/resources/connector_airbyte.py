# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json

import jsonschema

from instill.clients import InstillClient
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema import airbyte


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

        jsonschema.validate(
            vars(config), AirbyteAmazonsqsConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteAwsdatalakeConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteAzureblobstorageConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteBigqueryConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteCassandraConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteChromaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteClickhouseConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteConvexConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteCsvConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteCumulioConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteDatabendConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteDatabricksConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteDorisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteDuckdbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteDynamodbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteE2etestConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteElasticsearchConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteExasolConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteFireboltConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteFirestoreConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteGcsConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteGooglesheetsConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteIcebergConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteKafkaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteKeenConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteKinesisConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteLangchainConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteLocaljsonConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteMariadbcolumnstoreConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteMeilisearchConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteMilvusConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteMongodbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteMqttConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbytMssqlConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteMysqlConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteOracleConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbytePineconeConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbytePostgresConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbytePubsubConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbytePulsarConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteQdrantConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteR2Connector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteRabbitmqConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteRedisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteRedpandaConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteRedshiftConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteRocksetConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteS3glueConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteS3Connector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteScyllaConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteSelectdbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteSftpjsonConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteSnowflakeConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteSqliteConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteStarburstgalaxyConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteTeradataConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteTidbConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteTimeplusConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteTypesenseConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteVerticaConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteWeaviateConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(vars(config), AirbyteXataConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteYugabytedbConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


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

        jsonschema.validate(
            vars(config), AirbyteAirbytedevmatecloudConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))

# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json

import jsonschema

from instill.clients import InstillClient
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema import (
    bigquery,
    googlecloudstorage,
    googlesearch,
    pinecone,
    redis,
    restapi,
    website,
)


class BigQueryConnector(Connector):
    """BigQuery Connector"""

    with open(
        f"{const.SPEC_PATH}/bigquery_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: bigquery.BigQueryConnectorSpec,
    ) -> None:
        definition = "connector-definitions/bigquery"

        jsonschema.validate(vars(config), BigQueryConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class PineconeConnector(Connector):
    """Pinecone Connector"""

    with open(
        f"{const.SPEC_PATH}/pinecone_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: pinecone.PineconeConnectorSpec,
    ) -> None:
        definition = "connector-definitions/pinecone"

        jsonschema.validate(vars(config), PineconeConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class GoogleCloudStorageConnector(Connector):
    """GoogleCloudStorage Connector"""

    with open(
        f"{const.SPEC_PATH}/googlecloudstorage_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: googlecloudstorage.GoogleCloudStorageConnectorSpec,
    ) -> None:
        definition = "connector-definitions/gcs"

        jsonschema.validate(
            vars(config), GoogleCloudStorageConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, vars(config))


class GoogleSearchConnector(Connector):
    """GoogleSearch Connector"""

    with open(
        f"{const.SPEC_PATH}/googlecloudstorage_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: googlesearch.GoogleSearchConnectorSpec,
    ) -> None:
        definition = "connector-definitions/google-search"

        jsonschema.validate(vars(config), GoogleSearchConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class RedisConnector(Connector):
    """Redis Connector"""

    with open(f"{const.SPEC_PATH}/redis_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: redis.RedisConnectorResource,
    ) -> None:
        definition = "connector-definitions/redis"

        jsonschema.validate(vars(config), RedisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class RestAPIConnector(Connector):
    """RestAPI Connector"""

    with open(f"{const.SPEC_PATH}/restapi_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: restapi.RESTAPIConnectorSpec,
    ) -> None:
        definition = "connector-definitions/restapi"

        jsonschema.validate(vars(config), RestAPIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))


class WebsiteConnector(Connector):
    """Website Connector"""

    with open(f"{const.SPEC_PATH}/website_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: website.WebsiteConnectorResource,
    ) -> None:
        definition = "connector-definitions/website"

        jsonschema.validate(vars(config), WebsiteConnector.definitions_jsonschema)
        super().__init__(client, name, definition, vars(config))

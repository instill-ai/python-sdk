# pylint: disable=no-member,wrong-import-position,no-name-in-module
import json
from typing import Union

import jsonschema

from instill.clients import InstillClient
from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import Component
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema import (
    bigquery,
    bigquery_task_insert_input,
    googlecloudstorage,
    googlecloudstorage_task_upload_input,
    googlesearch,
    googlesearch_task_search_input,
    helper,
    pinecone,
    pinecone_task_query_input,
    pinecone_task_upsert_input,
    redis,
    redis_task_chat_history_retrieve_input,
    redis_task_chat_message_write_input,
    redis_task_chat_message_write_multi_modal_input,
    restapi,
    restapi_task_delete_input,
    restapi_task_get_input,
    restapi_task_head_input,
    restapi_task_options_input,
    restapi_task_patch_input,
    restapi_task_post_input,
    restapi_task_put_input,
    website,
    website_task_scrape_website_input,
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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, BigQueryConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: bigquery_task_insert_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, PineconeConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: Union[
            pinecone_task_query_input.Input,
            pinecone_task_upsert_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(
            config_spec, GoogleCloudStorageConnector.definitions_jsonschema
        )
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: googlecloudstorage_task_upload_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, GoogleSearchConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: googlesearch_task_search_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, RedisConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: Union[
            redis_task_chat_history_retrieve_input.Input,
            redis_task_chat_message_write_input.Input,
            redis_task_chat_message_write_multi_modal_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, RestAPIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: Union[
            restapi_task_delete_input.Input,
            restapi_task_options_input.Input,
            restapi_task_get_input.Input,
            restapi_task_head_input.Input,
            restapi_task_patch_input.Input,
            restapi_task_post_input.Input,
            restapi_task_patch_input.Input,
            restapi_task_put_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


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

        config_spec = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_spec, WebsiteConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_spec)

    def create_component(
        self,
        name: str,
        inp: website_task_scrape_website_input.Input,
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)

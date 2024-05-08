# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Union

from instill.resources import Component
from instill.resources.schema import (
    bigquery_task_insert_input,
    googlecloudstorage_task_upload_input,
    googlesearch_task_search_input,
    helper,
    pinecone_task_query_input,
    pinecone_task_upsert_input,
    redis_task_chat_history_retrieve_input,
    redis_task_chat_message_write_input,
    redis_task_chat_message_write_multi_modal_input,
    restapi_task_delete_input,
    restapi_task_get_input,
    restapi_task_head_input,
    restapi_task_options_input,
    restapi_task_patch_input,
    restapi_task_post_input,
    restapi_task_put_input,
    website_task_scrape_website_input,
)


class BigQueryConnector(Component):
    """BigQuery Connector"""

    def __init__(
        self,
        name: str,
        inp: bigquery_task_insert_input.Input,
    ) -> None:
        definition_name = "connector-definitions/bigquery"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class PineconeConnector(Component):
    """Pinecone Connector"""

    def __init__(
        self,
        name: str,
        inp: Union[
            pinecone_task_query_input.Input,
            pinecone_task_upsert_input.Input,
        ],
    ) -> None:
        definition_name = "connector-definitions/pinecone"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class GoogleCloudStorageConnector(Component):
    """GoogleCloudStorage Connector"""

    def __init__(
        self,
        name: str,
        inp: googlecloudstorage_task_upload_input.Input,
    ) -> None:
        definition_name = "connector-definitions/gcs"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class GoogleSearchConnector(Component):
    """GoogleSearch Connector"""

    def __init__(
        self,
        name: str,
        inp: googlesearch_task_search_input.Input,
    ) -> None:
        definition_name = "connector-definitions/google-search"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class RedisConnector(Component):
    """Redis Connector"""

    def __init__(
        self,
        name: str,
        inp: Union[
            redis_task_chat_history_retrieve_input.Input,
            redis_task_chat_message_write_input.Input,
            redis_task_chat_message_write_multi_modal_input.Input,
        ],
    ) -> None:
        definition_name = "connector-definitions/redis"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class RestAPIConnector(Component):
    """RestAPI Connector"""

    def __init__(
        self,
        name: str,
        inp: Union[
            restapi_task_delete_input.Input,
            restapi_task_options_input.Input,
            restapi_task_get_input.InputWithoutBody,
            restapi_task_head_input.InputWithoutBody,
            restapi_task_patch_input.Input,
            restapi_task_post_input.Input,
            restapi_task_patch_input.Input,
            restapi_task_put_input.Input,
        ],
    ) -> None:
        definition_name = "connector-definitions/restapi"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class WebsiteConnector(Component):
    """Website Connector"""

    def __init__(
        self,
        name: str,
        inp: website_task_scrape_website_input.Input,
    ) -> None:
        definition_name = "connector-definitions/website"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)

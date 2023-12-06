# pylint: disable=no-member,wrong-import-position,no-name-in-module
from instill.clients import InstillClient
from instill.resources.connector import Connector


class NumbersConnector(Connector):
    def __init__(
        self,
        client: InstillClient,
        name: str,
        capture_token: str,
        asset_type: str,
        metadata_texts: bool,
        metadata_structured_data: bool,
        metadata_metadata: bool,
    ) -> None:
        definition = "connector-definitions/numbers"
        configuration = {
            "capture_token": capture_token,
            "asset_type": asset_type,
            "metadata_texts": metadata_texts,
            "metadata_structured_data": metadata_structured_data,
            "metadata_metadata": metadata_metadata,
        }
        super().__init__(client, name, definition, configuration)

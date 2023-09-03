# pylint: disable=no-member,wrong-import-position
from instill_sdk.clients.connector import ConnectorClient
from instill_sdk.resources.connector import Connector


class NumbersConnector(Connector):
    def __init__(
        self,
        client: ConnectorClient,
        name: str,
        capture_token: str,
        asset_type: str,
        metadata_texts: bool,
        metadata_structured_data: bool,
        metadata_metadata: bool,
    ) -> None:
        definition = "connector-definitions/blockchain-numbers"
        configuration = {
            "capture_token": capture_token,
            "asset_type": asset_type,
            "metadata_texts": metadata_texts,
            "metadata_structured_data": metadata_structured_data,
            "metadata_metadata": metadata_metadata,
        }
        super().__init__(client, name, definition, configuration)

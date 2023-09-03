"""Integration tests configuration file."""
# pylint: disable=unused-import

import pytest

from instill_sdk.clients.connector import ConnectorClient
from instill_sdk.clients.mgmt import MgmtClient
from instill_sdk.clients.model import ModelClient
from instill_sdk.clients.pipeline import PipelineClient
from instill_sdk.tests.conftest import pytest_configure


@pytest.fixture(scope="session")
def clients():
    pass
    # mgmt_client = MgmtClient()
    # model_client = ModelClient(user=mgmt_client.get_user())
    # connector_client = ConnectorClient(user=mgmt_client.get_user())
    # pipeline_client = PipelineClient(user=mgmt_client.get_user())

    # return [mgmt_client, model_client, connector_client, pipeline_client]

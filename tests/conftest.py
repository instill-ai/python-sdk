"""Integration tests configuration file."""
# pylint: disable=unused-import,no-name-in-module

import pytest

from instill.clients import ConnectorClient, MgmtClient, ModelClient, PipelineClient
from instill.tests.conftest import pytest_configure


@pytest.fixture(scope="session")
def clients():
    pass
    # mgmt_client = MgmtClient()
    # model_client = ModelClient(user=mgmt_client.get_user())
    # connector_client = ConnectorClient(user=mgmt_client.get_user())
    # pipeline_client = PipelineClient(user=mgmt_client.get_user())

    # return [mgmt_client, model_client, connector_client, pipeline_client]

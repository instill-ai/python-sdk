"""Integration tests configuration file."""

# pylint: disable=unused-import,no-name-in-module

import pytest

from instill.clients import MgmtClient, ModelClient, PipelineClient
from instill.tests.conftest import pytest_configure


@pytest.fixture(scope="session")
def clients():
    pass
    # mgmt_client = MgmtClient()
    # model_client = ModelClient(user=mgmt_client.get_user())
    # pipeline_client = PipelineClient(user=mgmt_client.get_user())

    # return [mgmt_client, model_client, pipeline_client]

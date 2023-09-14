# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned


from instill_sdk.clients.connector import ConnectorClient
from instill_sdk.clients.mgmt import MgmtClient
from instill_sdk.clients.model import ModelClient
from instill_sdk.clients.pipeline import PipelineClient


def describe_client():
    def describe_host():
        def when_not_set(expect):
            mgmt_client = MgmtClient()
            expect(mgmt_client.host) == "localhost"
            model_client = ModelClient(user=mgmt_client.get_user())
            expect(model_client.host) == "localhost"
            pipeline_client = PipelineClient(user=mgmt_client.get_user())
            expect(pipeline_client.host) == "localhost"
            connector_client = ConnectorClient(user=mgmt_client.get_user())
            expect(connector_client.host) == "localhost"

        def when_set_correct_type(expect):
            mgmt_client = MgmtClient()
            mgmt_client.host = "instill"
            expect(mgmt_client.host) == "instill"
            model_client = ModelClient(user=mgmt_client.get_user())
            model_client.host = "instill"
            expect(model_client.host) == "instill"
            pipeline_client = PipelineClient(user=mgmt_client.get_user())
            pipeline_client.host = "instill"
            expect(pipeline_client.host) == "instill"
            connector_client = ConnectorClient(user=mgmt_client.get_user())
            connector_client.host = "instill"
            expect(connector_client.host) == "instill"

    def describe_token():
        def when_not_set(expect):
            mgmt_client = MgmtClient()
            expect(mgmt_client.token) == ""
            model_client = ModelClient(user=mgmt_client.get_user())
            expect(model_client.token) == ""
            pipeline_client = PipelineClient(user=mgmt_client.get_user())
            expect(pipeline_client.token) == ""
            connector_client = ConnectorClient(user=mgmt_client.get_user())
            expect(connector_client.token) == ""

        def when_set_correct_type(expect):
            mgmt_client = MgmtClient()
            mgmt_client.token = "instill"
            expect(mgmt_client.token) == "instill"
            model_client = ModelClient(user=mgmt_client.get_user())
            model_client.token = "instill"
            expect(model_client.token) == "instill"
            pipeline_client = PipelineClient(user=mgmt_client.get_user())
            pipeline_client.token = "instill"
            expect(pipeline_client.token) == "instill"
            connector_client = ConnectorClient(user=mgmt_client.get_user())
            connector_client.token = "instill"
            expect(connector_client.token) == "instill"

    def describe_port():
        def when_not_set(expect):
            mgmt_client = MgmtClient()
            expect(mgmt_client.port) == "7080"
            model_client = ModelClient(user=mgmt_client.get_user())
            expect(model_client.port) == "9080"
            pipeline_client = PipelineClient(user=mgmt_client.get_user())
            expect(pipeline_client.port) == "8080"
            connector_client = ConnectorClient(user=mgmt_client.get_user())
            expect(connector_client.port) == "8080"

        def when_set_correct_type(expect):
            mgmt_client = MgmtClient()
            mgmt_client.port = "instill"
            expect(mgmt_client.port) == "instill"
            model_client = ModelClient(user=mgmt_client.get_user())
            model_client.port = "instill"
            expect(model_client.port) == "instill"
            pipeline_client = PipelineClient(user=mgmt_client.get_user())
            pipeline_client.port = "instill"
            expect(pipeline_client.port) == "instill"
            connector_client = ConnectorClient(user=mgmt_client.get_user())
            connector_client.port = "instill"
            expect(connector_client.port) == "instill"

# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,no-name-in-module

from collections import defaultdict

from instill.clients import ConnectorClient, MgmtClient, ModelClient, PipelineClient


def describe_client():
    def describe_instance():
        def when_not_set(expect):
            mgmt_client = MgmtClient()
            expect(mgmt_client.instance) == ""
            model_client = ModelClient(namespace="")
            expect(model_client.instance) == ""
            pipeline_client = PipelineClient(namespace="")
            expect(pipeline_client.instance) == ""
            connector_client = ConnectorClient(namespace="")
            expect(connector_client.instance) == ""

        def when_set_correct_type(expect):
            mgmt_client = MgmtClient()
            mgmt_client.instance = "staging"
            expect(mgmt_client.instance) == "staging"
            model_client = ModelClient(namespace="")
            model_client.instance = "staging"
            expect(model_client.instance) == "staging"
            pipeline_client = PipelineClient(namespace="")
            pipeline_client.instance = "staging"
            expect(pipeline_client.instance) == "staging"
            connector_client = ConnectorClient(namespace="")
            connector_client.instance = "staging"
            expect(connector_client.instance) == "staging"

    def describe_host():
        def when_not_set(expect):
            mgmt_client = MgmtClient()
            expect(mgmt_client.hosts) is None
            model_client = ModelClient(namespace="")
            expect(model_client.hosts) is None
            pipeline_client = PipelineClient(namespace="")
            expect(pipeline_client.hosts) is None
            connector_client = ConnectorClient(namespace="")
            expect(connector_client.hosts) is None

        def when_set_correct_type(expect):
            mgmt_client = MgmtClient()
            d = defaultdict(dict)  # type: ignore
            d["test_instance"] = dict({"url": "test_url"})
            mgmt_client.hosts = d
            expect(mgmt_client.hosts["test_instance"]["url"]) == "test_url"
            model_client = ModelClient(namespace="")
            model_client.hosts = d
            expect(model_client.hosts["test_instance"]["url"]) == "test_url"
            pipeline_client = PipelineClient(namespace="")
            pipeline_client.hosts = d
            expect(pipeline_client.hosts["test_instance"]["url"]) == "test_url"
            connector_client = ConnectorClient(namespace="")
            connector_client.hosts = d
            expect(connector_client.hosts["test_instance"]["url"]) == "test_url"

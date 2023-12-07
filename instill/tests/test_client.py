# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,no-name-in-module

import instill.protogen.core.mgmt.v1beta.mgmt_public_service_pb2_grpc as mgmt_service
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
import instill.protogen.vdp.pipeline.v1beta.pipeline_public_service_pb2_grpc as pipeline_service
from instill.clients import MgmtClient, ModelClient, PipelineClient
from instill.clients.instance import InstillInstance


def describe_client():
    def describe_instance():
        def when_not_set(expect):
            mgmt_client = MgmtClient(False)
            expect(mgmt_client.instance) == ""
            model_client = ModelClient(namespace="", async_enabled=False)
            expect(model_client.instance) == ""
            pipeline_client = PipelineClient(namespace="", async_enabled=False)
            expect(pipeline_client.instance) == ""

        def when_set_correct_type(expect):
            mgmt_client = MgmtClient(False)
            mgmt_client.instance = "staging"
            expect(mgmt_client.instance) == "staging"
            model_client = ModelClient(namespace="", async_enabled=False)
            model_client.instance = "staging"
            expect(model_client.instance) == "staging"
            pipeline_client = PipelineClient(namespace="", async_enabled=False)
            pipeline_client.instance = "staging"
            expect(pipeline_client.instance) == "staging"

    def describe_host():
        def when_not_set(expect):
            mgmt_client = MgmtClient(False)
            expect(mgmt_client.hosts) is None
            model_client = ModelClient(namespace="", async_enabled=False)
            expect(model_client.hosts) is None
            pipeline_client = PipelineClient(namespace="", async_enabled=False)
            expect(pipeline_client.hosts) is None

        def when_set_correct_type_url(expect):
            mgmt_instance = {
                "test_instance": InstillInstance(
                    mgmt_service.MgmtPublicServiceStub,
                    "test_url",
                    "token",
                    False,
                    False,
                )
            }
            mgmt_client = MgmtClient(False)
            mgmt_client.hosts = mgmt_instance
            expect(mgmt_client.hosts["test_instance"].url) == "test_url"

            model_instance = {
                "test_instance": InstillInstance(
                    model_service.ModelPublicServiceStub,
                    "test_url",
                    "token",
                    False,
                    False,
                )
            }
            model_client = ModelClient(namespace="", async_enabled=False)
            model_client.hosts = model_instance
            expect(model_client.hosts["test_instance"].url) == "test_url"

            pipeline_instance = {
                "test_instance": InstillInstance(
                    pipeline_service.PipelinePublicServiceStub,
                    "test_url",
                    "token",
                    False,
                    False,
                )
            }
            pipeline_client = PipelineClient(namespace="", async_enabled=False)
            pipeline_client.hosts = pipeline_instance
            expect(pipeline_client.hosts["test_instance"].url) == "test_url"

        def when_set_correct_type_token(expect):
            mgmt_instance = {
                "test_instance": InstillInstance(
                    mgmt_service.MgmtPublicServiceStub,
                    "test_url",
                    "token",
                    False,
                    False,
                )
            }
            mgmt_client = MgmtClient(False)
            mgmt_client.hosts = mgmt_instance
            expect(mgmt_client.hosts["test_instance"].token) == "token"

            model_instance = {
                "test_instance": InstillInstance(
                    model_service.ModelPublicServiceStub,
                    "test_url",
                    "token",
                    False,
                    False,
                )
            }
            model_client = ModelClient(namespace="", async_enabled=False)
            model_client.hosts = model_instance
            expect(model_client.hosts["test_instance"].token) == "token"

            pipeline_instance = {
                "test_instance": InstillInstance(
                    pipeline_service.PipelinePublicServiceStub,
                    "test_url",
                    "token",
                    False,
                    False,
                )
            }
            pipeline_client = PipelineClient(namespace="", async_enabled=False)
            pipeline_client.hosts = pipeline_instance
            expect(pipeline_client.hosts["test_instance"].token) == "token"

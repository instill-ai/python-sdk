# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,no-name-in-module

import instill.protogen.core.mgmt.v1beta.mgmt_public_service_pb2_grpc as mgmt_service
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
import instill.protogen.vdp.pipeline.v1beta.pipeline_public_service_pb2_grpc as pipeline_service
from instill.clients import MgmtClient, ModelClient, PipelineClient
from instill.clients.instance import InstillInstance


def mock(_: str):
    return ""


def describe_client():
    def describe_host():
        def when_not_set(expect):
            mgmt_client = MgmtClient("")
            expect(mgmt_client.host) is not None
            model_client = ModelClient("", mock)
            expect(model_client.host) is not None
            pipeline_client = PipelineClient("", mock)
            expect(pipeline_client.host) is not None

        def when_set_correct_type_url(expect):
            mgmt_instance = InstillInstance(
                mgmt_service.MgmtPublicServiceStub,
                "test_url",
                "token",
                False,
                False,
            )
            mgmt_client = MgmtClient("")
            mgmt_client.host = mgmt_instance
            expect(mgmt_client.host.url) == "test_url"

            model_instance = InstillInstance(
                model_service.ModelPublicServiceStub,
                "test_url",
                "token",
                False,
                False,
            )
            model_client = ModelClient("", mock)
            model_client.host = model_instance
            expect(model_client.host.url) == "test_url"

            pipeline_instance = InstillInstance(
                pipeline_service.PipelinePublicServiceStub,
                "test_url",
                "token",
                False,
                False,
            )
            pipeline_client = PipelineClient("", mock)
            pipeline_client.host = pipeline_instance
            expect(pipeline_client.host.url) == "test_url"

        def when_set_correct_type_token(expect):
            mgmt_instance = InstillInstance(
                mgmt_service.MgmtPublicServiceStub,
                "test_url",
                "token",
                False,
                False,
            )
            mgmt_client = MgmtClient("")
            mgmt_client.host = mgmt_instance
            expect(mgmt_client.host.token) == "token"

            model_instance = InstillInstance(
                model_service.ModelPublicServiceStub,
                "test_url",
                "token",
                False,
                False,
            )
            model_client = ModelClient("", mock)
            model_client.host = model_instance
            expect(model_client.host.token) == "token"

            pipeline_instance = InstillInstance(
                pipeline_service.PipelinePublicServiceStub,
                "test_url",
                "token",
                False,
                False,
            )
            pipeline_client = PipelineClient("", mock)
            pipeline_client.host = pipeline_instance
            expect(pipeline_client.host.token) == "token"

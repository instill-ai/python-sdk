from typing import Union
import grpc


import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
import instill.protogen.vdp.pipeline.v1alpha.pipeline_public_service_pb2_grpc as pipeline_service
import instill.protogen.core.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service


class InstillInstance:
    def __init__(self, url: str, token: str, secure: bool, stub):
        self.token: str = token
        if not secure:
            channel = grpc.insecure_channel(url)
            async_channel = grpc.aio.insecure_channel(url)
            self.metadata = (
                (
                    "authorization",
                    f"Bearer {token}",
                ),
            )
        else:
            ssl_creds = grpc.ssl_channel_credentials()
            call_creds = grpc.access_token_call_credentials(token)
            creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
            channel = grpc.secure_channel(target=url, credentials=creds)
            async_channel = grpc.aio.secure_channel(target=url, credentials=creds)
            self.metadata = ""
        self.channel: grpc.Channel = channel
        self.async_channel: grpc.Channel = async_channel
        self.client: Union[
            model_service.ModelPublicServiceStub,
            pipeline_service.PipelinePublicServiceStub,
            mgmt_service.MgmtPublicServiceStub,
        ] = stub(channel)
        self.async_client: Union[
            model_service.ModelPublicServiceStub,
            pipeline_service.PipelinePublicServiceStub,
            mgmt_service.MgmtPublicServiceStub,
        ] = stub(async_channel)

from typing import Union

import grpc

import instill.protogen.core.mgmt.v1alpha.mgmt_public_service_pb2_grpc as mgmt_service
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
import instill.protogen.vdp.pipeline.v1alpha.pipeline_public_service_pb2_grpc as pipeline_service


class InstillInstance:
    def __init__(self, stub, url: str, token: str, secure: bool, asyncio: bool):
        self.url: str = url
        self.token: str = token
        self.asyncio: bool = asyncio
        if not secure:
            channel = grpc.insecure_channel(url)
            self.metadata = (
                (
                    "authorization",
                    f"Bearer {token}",
                ),
            )
            if asyncio:
                async_channel = grpc.aio.insecure_channel(url)
        else:
            ssl_creds = grpc.ssl_channel_credentials()
            call_creds = grpc.access_token_call_credentials(token)
            creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
            channel = grpc.secure_channel(target=url, credentials=creds)
            self.metadata = (("", ""),)
            if asyncio:
                async_channel = grpc.aio.secure_channel(target=url, credentials=creds)
        self.channel: grpc.Channel = channel
        self.client: Union[
            model_service.ModelPublicServiceStub,
            pipeline_service.PipelinePublicServiceStub,
            mgmt_service.MgmtPublicServiceStub,
        ] = stub(channel)
        if asyncio:
            self.async_channel: grpc.Channel = async_channel
            self.async_client: Union[
                model_service.ModelPublicServiceStub,
                pipeline_service.PipelinePublicServiceStub,
                mgmt_service.MgmtPublicServiceStub,
            ] = stub(async_channel)

from typing import Union

import grpc

import instill.protogen.artifact.artifact.v1alpha.artifact_public_service_pb2_grpc as artifact_service
import instill.protogen.core.mgmt.v1beta.mgmt_public_service_pb2_grpc as mgmt_service
import instill.protogen.model.model.v1alpha.model_public_service_pb2_grpc as model_service
import instill.protogen.vdp.pipeline.v1beta.pipeline_public_service_pb2_grpc as pipeline_service

MB = 1024**2


class InstillInstance:
    def __init__(self, stub, url: str, token: str, secure: bool, async_enabled: bool):
        self.url: str = url
        self.token: str = token
        self.async_enabled: bool = async_enabled
        self.metadata: Union[str, tuple] = ""

        channel_options = (
            ("grpc.max_send_message_length", 32 * MB),
            ("grpc.max_receive_message_length", 32 * MB),
        )

        if not secure:
            channel = grpc.insecure_channel(url, options=channel_options)
            self.metadata = (
                (
                    "authorization",
                    f"Bearer {token}",
                ),
            )
            if async_enabled:
                async_channel = grpc.aio.insecure_channel(url, options=channel_options)
        else:
            ssl_creds = grpc.ssl_channel_credentials()
            call_creds = grpc.access_token_call_credentials(token)
            creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
            channel = grpc.secure_channel(
                target=url, credentials=creds, options=channel_options
            )
            if async_enabled:
                async_channel = grpc.aio.secure_channel(
                    target=url, credentials=creds, options=channel_options
                )
        self.channel: grpc.Channel = channel
        self.client: Union[
            model_service.ModelPublicServiceStub,
            pipeline_service.PipelinePublicServiceStub,
            mgmt_service.MgmtPublicServiceStub,
            artifact_service.ArtifactPublicServiceStub,
        ] = stub(channel)
        if async_enabled:
            self.async_channel: grpc.Channel = async_channel
            self.async_client: Union[
                model_service.ModelPublicServiceStub,
                pipeline_service.PipelinePublicServiceStub,
                mgmt_service.MgmtPublicServiceStub,
                artifact_service.ArtifactPublicServiceStub,
            ] = stub(async_channel)

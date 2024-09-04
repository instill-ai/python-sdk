# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from typing import Dict

# artifact
import instill.protogen.artifact.artifact.v1alpha.artifact_pb2 as artifact_interface
import instill.protogen.artifact.artifact.v1alpha.artifact_public_service_pb2_grpc as artifact_service
import instill.protogen.artifact.artifact.v1alpha.chunk_pb2 as chunk_interface
import instill.protogen.artifact.artifact.v1alpha.conversation_pb2 as conversation_interface
import instill.protogen.artifact.artifact.v1alpha.file_catalog_pb2 as file_catalog_interface
import instill.protogen.artifact.artifact.v1alpha.qa_pb2 as qa_interface

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler


class ArtifactClient(Client):
    def __init__(self, async_enabled: bool = False, api_token: str = "") -> None:
        self.hosts: Dict[str, InstillInstance] = {}
        if DEFAULT_INSTANCE in global_config.hosts:
            self.instance = DEFAULT_INSTANCE
        elif len(global_config.hosts) == 0:
            self.instance = ""
        else:
            self.instance = list(global_config.hosts.keys())[0]

        if global_config.hosts is not None:
            for instance, config in global_config.hosts.items():
                token = config.token
                if api_token != "" and instance == self.instance:
                    token = api_token
                self.hosts[instance] = InstillInstance(
                    artifact_service.ArtifactPublicServiceStub,
                    url=config.url,
                    token=token,
                    secure=config.secure,
                    async_enabled=async_enabled,
                )

    def close(self):
        if self.is_serving():
            for host in self.hosts.values():
                host.channel.close()

    async def async_close(self):
        if self.is_serving():
            for host in self.hosts.values():
                await host.async_channel.close()

    @property
    def hosts(self):
        return self._hosts

    @hosts.setter
    def hosts(self, hosts: Dict[str, InstillInstance]):
        self._hosts = hosts

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, instance: str):
        self._instance = instance

    def set_instance(self, instance: str):
        self._instance = instance

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: str):
        self._metadata = metadata

    def liveness(
        self,
        async_enabled: bool = False,
    ) -> artifact_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Liveness,
                request=artifact_interface.LivenessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Liveness,
            request=artifact_interface.LivenessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    def readiness(
        self,
        async_enabled: bool = False,
    ) -> artifact_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Readiness,
                request=artifact_interface.ReadinessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Readiness,
            request=artifact_interface.ReadinessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    def is_serving(self) -> bool:
        try:
            return (
                self.readiness().health_check_response.status
                == healthcheck.HealthCheckResponse.SERVING_STATUS_SERVING
            )
        except Exception:
            return False

    @grpc_handler
    def create_catalog(
        self,
        namespace_id: str,
        name: str,
        description: str,
        tags: list[str],
        async_enabled: bool = False,
    ) -> artifact_interface.CreateCatalogResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateCatalog,
                request=artifact_interface.CreateCatalogRequest(
                    namespace_id=namespace_id,
                    name=name,
                    description=description,
                    tags=tags,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateCatalog,
            request=artifact_interface.CreateCatalogRequest(
                namespace_id=namespace_id,
                name=name,
                description=description,
                tags=tags,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_catalogs(
        self,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.ListCatalogsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListCatalogs,
                request=artifact_interface.ListCatalogsRequest(
                    namespace_id=namespace_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListCatalogs,
            request=artifact_interface.ListCatalogsRequest(
                namespace_id=namespace_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_catalog(
        self,
        catalog_id: str,
        description: str,
        tags: list[str],
        namespace_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.UpdateCatalogResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateCatalog,
                request=artifact_interface.UpdateCatalogRequest(
                    catalog_id=catalog_id,
                    description=description,
                    tags=tags,
                    namespace_id=namespace_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateCatalog,
            request=artifact_interface.UpdateCatalogRequest(
                catalog_id=catalog_id,
                description=description,
                tags=tags,
                namespace_id=namespace_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_catalog(
        self,
        namespace_id: str,
        catalog_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.DeleteCatalogResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteCatalog,
                request=artifact_interface.DeleteCatalogRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteCatalog,
            request=artifact_interface.DeleteCatalogRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def upload_catalog_file(
        self,
        namespace_id: str,
        catalog_id: str,
        file: artifact_interface.File,
        async_enabled: bool = False,
    ) -> artifact_interface.UploadCatalogFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UploadCatalogFile,
                request=artifact_interface.UploadCatalogFileRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file=file,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UploadCatalogFile,
            request=artifact_interface.UploadCatalogFileRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file=file,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_catalog_file(
        self,
        file_uid: str,
        async_enabled: bool = False,
    ) -> artifact_interface.DeleteCatalogFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteCatalogFile,
                request=artifact_interface.DeleteCatalogFileRequest(
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteCatalogFile,
            request=artifact_interface.DeleteCatalogFileRequest(
                file_uid=file_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def process_catalog_files(
        self,
        file_uids: list[str],
        async_enabled: bool = False,
    ) -> artifact_interface.ProcessCatalogFilesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ProcessCatalogFiles,
                request=artifact_interface.ProcessCatalogFilesRequest(
                    file_uids=file_uids,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ProcessCatalogFiles,
            request=artifact_interface.ProcessCatalogFilesRequest(
                file_uids=file_uids,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_catalog_files(
        self,
        namespace_id: str,
        catalog_id: str,
        files_filter: list[str],
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> artifact_interface.ListCatalogFilesResponse:
        list_catalog_files_filter = artifact_interface.ListCatalogFilesFilter()
        for file_uid in files_filter:
            list_catalog_files_filter.file_uids.append(file_uid)

        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListCatalogFiles,
                request=artifact_interface.ListCatalogFilesRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    filter=list_catalog_files_filter,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListCatalogFiles,
            request=artifact_interface.ListCatalogFilesRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                filter=list_catalog_files_filter,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_chunks(
        self,
        namespace_id: str,
        catalog_id: str,
        file_uid: str,
        async_enabled: bool = False,
    ) -> chunk_interface.ListChunksResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListChunks,
                request=chunk_interface.ListChunksRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListChunks,
            request=chunk_interface.ListChunksRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file_uid=file_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_source_file(
        self,
        namespace_id: str,
        catalog_id: str,
        file_uid: str,
        async_enabled: bool = False,
    ) -> chunk_interface.GetSourceFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetSourceFile,
                request=chunk_interface.GetSourceFileRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetSourceFile,
            request=chunk_interface.GetSourceFileRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file_uid=file_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_chunk(
        self,
        chunk_uid: str,
        retrievable: bool,
        async_enabled: bool = False,
    ) -> chunk_interface.UpdateChunkResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateChunk,
                request=chunk_interface.UpdateChunkRequest(
                    chunk_uid=chunk_uid,
                    retrievable=retrievable,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateChunk,
            request=chunk_interface.UpdateChunkRequest(
                chunk_uid=chunk_uid,
                retrievable=retrievable,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def similarity_chunks_search(
        self,
        namespace_id: str,
        catalog_id: str,
        text_prompt: str,
        top_k: int,
        async_enabled: bool = False,
    ) -> chunk_interface.SimilarityChunksSearchResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.SimilarityChunksSearch,
                request=chunk_interface.SimilarityChunksSearchRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    text_prompt=text_prompt,
                    top_k=top_k,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.SimilarityChunksSearch,
            request=chunk_interface.SimilarityChunksSearchRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                text_prompt=text_prompt,
                top_k=top_k,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def question_answering(
        self,
        namespace_id: str,
        catalog_id: str,
        question: str,
        top_k: int,
        async_enabled: bool = False,
    ) -> qa_interface.QuestionAnsweringResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.QuestionAnswering,
                request=qa_interface.QuestionAnsweringRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    question=question,
                    top_k=top_k,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.QuestionAnswering,
            request=qa_interface.QuestionAnsweringRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                question=question,
                top_k=top_k,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_file_catalog(
        self,
        namespace_id: str,
        catalog_id: str,
        file_id: str,
        file_uid: str,
        async_enabled: bool = False,
    ) -> file_catalog_interface.GetFileCatalogResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetFileCatalog,
                request=file_catalog_interface.GetFileCatalogRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file_id=file_id,
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetFileCatalog,
            request=file_catalog_interface.GetFileCatalogRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file_id=file_id,
                file_uid=file_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_conversation(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        async_enabled: bool = False,
    ) -> conversation_interface.CreateConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateConversation,
                request=conversation_interface.CreateConversationRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateConversation,
            request=conversation_interface.CreateConversationRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_conversations(
        self,
        namespace_id: str,
        catalog_id: str,
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> conversation_interface.ListConversationsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListConversations,
                request=conversation_interface.ListConversationsRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListConversations,
            request=conversation_interface.ListConversationsRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_conversation(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        new_conversation_id: str,
        async_enabled: bool = False,
    ) -> conversation_interface.UpdateConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateConversation,
                request=conversation_interface.UpdateConversationRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    new_conversation_id=new_conversation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateConversation,
            request=conversation_interface.UpdateConversationRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                new_conversation_id=new_conversation_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_conversation(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        async_enabled: bool = False,
    ) -> conversation_interface.DeleteConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteConversation,
                request=conversation_interface.DeleteConversationRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteConversation,
            request=conversation_interface.DeleteConversationRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def create_message(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        content: str,
        role: str,
        async_enabled: bool = False,
    ) -> conversation_interface.CreateMessageResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateMessage,
                request=conversation_interface.CreateMessageRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    content=content,
                    role=role,
                    type=conversation_interface.Message.MessageType.MESSAGE_TYPE_TEXT,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateMessage,
            request=conversation_interface.CreateMessageRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                content=content,
                role=role,
                type=conversation_interface.Message.MessageType.MESSAGE_TYPE_TEXT,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_messages(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        latest_k: int,
        include_system_messages: bool,
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> conversation_interface.ListMessagesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListMessages,
                request=conversation_interface.ListMessagesRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    latest_k=latest_k,
                    include_system_messages=include_system_messages,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListMessages,
            request=conversation_interface.ListMessagesRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                latest_k=latest_k,
                include_system_messages=include_system_messages,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_message(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        message_uid: str,
        content: str,
        async_enabled: bool = False,
    ) -> conversation_interface.UpdateMessageResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateMessage,
                request=conversation_interface.UpdateMessageRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    message_uid=message_uid,
                    content=content,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateMessage,
            request=conversation_interface.UpdateMessageRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                message_uid=message_uid,
                content=content,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_message(
        self,
        namespace_id: str,
        catalog_id: str,
        conversation_id: str,
        message_uid: str,
        async_enabled: bool = False,
    ) -> conversation_interface.DeleteMessageResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteMessage,
                request=conversation_interface.DeleteMessageRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    message_uid=message_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteMessage,
            request=conversation_interface.DeleteMessageRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                message_uid=message_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

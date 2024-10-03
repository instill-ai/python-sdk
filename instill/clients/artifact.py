# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from typing import Callable, List, Optional

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
from instill.clients.instance import InstillInstance
from instill.utils.error_handler import grpc_handler
from instill.utils.process_file import process_file


class ArtifactClient(Client):
    def __init__(
        self,
        api_token: str,
        lookup_func: Callable[[str], str],
        url: str = "api.instill.tech",
        secure: bool = True,
        requester_id: str = "",
        async_enabled: bool = False,
    ) -> None:
        self.host: InstillInstance = InstillInstance(
            artifact_service.ArtifactPublicServiceStub,
            url=url,
            token=api_token,
            secure=secure,
            async_enabled=async_enabled,
        )
        self.metadata = []
        self._lookup_uid = lookup_func

        if requester_id != "":
            requester_uid = lookup_func(requester_id)
            self.metadata = [("instill-requester-uid", requester_uid)]

    def close(self):
        if self.is_serving():
            self.host.channel.close()

    async def async_close(self):
        if self.is_serving():
            self.host.channel.close()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host: InstillInstance):
        self._host = host

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: List[tuple]):
        self._metadata = metadata

    def liveness(
        self,
        async_enabled: bool = False,
    ) -> artifact_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Liveness,
                request=artifact_interface.LivenessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Liveness,
            request=artifact_interface.LivenessRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    def readiness(
        self,
        async_enabled: bool = False,
    ) -> artifact_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Readiness,
                request=artifact_interface.ReadinessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Readiness,
            request=artifact_interface.ReadinessRequest(),
            metadata=self.host.metadata + self.metadata,
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
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> artifact_interface.CreateCatalogResponse:
        tags = tags if tags is not None else []

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateCatalog,
                request=artifact_interface.CreateCatalogRequest(
                    namespace_id=namespace_id,
                    name=name,
                    description=description,
                    tags=tags,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateCatalog,
            request=artifact_interface.CreateCatalogRequest(
                namespace_id=namespace_id,
                name=name,
                description=description,
                tags=tags,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_catalogs(
        self,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.ListCatalogsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListCatalogs,
                request=artifact_interface.ListCatalogsRequest(
                    namespace_id=namespace_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListCatalogs,
            request=artifact_interface.ListCatalogsRequest(
                namespace_id=namespace_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_catalog(
        self,
        catalog_id: str,
        description: str,
        namespace_id: str,
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> artifact_interface.UpdateCatalogResponse:
        tags = tags if tags is not None else []

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateCatalog,
                request=artifact_interface.UpdateCatalogRequest(
                    catalog_id=catalog_id,
                    description=description,
                    tags=tags,
                    namespace_id=namespace_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateCatalog,
            request=artifact_interface.UpdateCatalogRequest(
                catalog_id=catalog_id,
                description=description,
                tags=tags,
                namespace_id=namespace_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.DeleteCatalog,
                request=artifact_interface.DeleteCatalogRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteCatalog,
            request=artifact_interface.DeleteCatalogRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def upload_catalog_file(
        self,
        namespace_id: str,
        catalog_id: str,
        file_path: str,
        async_enabled: bool = False,
    ) -> artifact_interface.UploadCatalogFileResponse:
        file = process_file(file_path)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UploadCatalogFile,
                request=artifact_interface.UploadCatalogFileRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file=file,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UploadCatalogFile,
            request=artifact_interface.UploadCatalogFileRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file=file,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_catalog_file(
        self,
        file_uid: str,
        async_enabled: bool = False,
    ) -> artifact_interface.DeleteCatalogFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteCatalogFile,
                request=artifact_interface.DeleteCatalogFileRequest(
                    file_uid=file_uid,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteCatalogFile,
            request=artifact_interface.DeleteCatalogFileRequest(
                file_uid=file_uid,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def process_catalog_files(
        self,
        file_uids: list[str],
        async_enabled: bool = False,
    ) -> artifact_interface.ProcessCatalogFilesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ProcessCatalogFiles,
                request=artifact_interface.ProcessCatalogFilesRequest(
                    file_uids=file_uids,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ProcessCatalogFiles,
            request=artifact_interface.ProcessCatalogFilesRequest(
                file_uids=file_uids,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_catalog_files(
        self,
        namespace_id: str,
        catalog_id: str,
        files_filter: Optional[list[str]] = None,
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> artifact_interface.ListCatalogFilesResponse:
        list_catalog_files_filter = artifact_interface.ListCatalogFilesFilter()
        files_filter = files_filter if files_filter is not None else []
        for file_uid in files_filter:
            list_catalog_files_filter.file_uids.append(file_uid)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListCatalogFiles,
                request=artifact_interface.ListCatalogFilesRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    filter=list_catalog_files_filter,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListCatalogFiles,
            request=artifact_interface.ListCatalogFilesRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                filter=list_catalog_files_filter,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListChunks,
                request=chunk_interface.ListChunksRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file_uid=file_uid,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListChunks,
            request=chunk_interface.ListChunksRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file_uid=file_uid,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.GetSourceFile,
                request=chunk_interface.GetSourceFileRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file_uid=file_uid,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetSourceFile,
            request=chunk_interface.GetSourceFileRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file_uid=file_uid,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.UpdateChunk,
                request=chunk_interface.UpdateChunkRequest(
                    chunk_uid=chunk_uid,
                    retrievable=retrievable,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateChunk,
            request=chunk_interface.UpdateChunkRequest(
                chunk_uid=chunk_uid,
                retrievable=retrievable,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.SimilarityChunksSearch,
                request=chunk_interface.SimilarityChunksSearchRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    text_prompt=text_prompt,
                    top_k=top_k,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.SimilarityChunksSearch,
            request=chunk_interface.SimilarityChunksSearchRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                text_prompt=text_prompt,
                top_k=top_k,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.QuestionAnswering,
                request=qa_interface.QuestionAnsweringRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    question=question,
                    top_k=top_k,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.QuestionAnswering,
            request=qa_interface.QuestionAnsweringRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                question=question,
                top_k=top_k,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_file_catalog(
        self,
        namespace_id: str,
        catalog_id: str,
        file_id: str = "",
        file_uid: str = "",
        async_enabled: bool = False,
    ) -> file_catalog_interface.GetFileCatalogResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetFileCatalog,
                request=file_catalog_interface.GetFileCatalogRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    file_id=file_id,
                    file_uid=file_uid,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetFileCatalog,
            request=file_catalog_interface.GetFileCatalogRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                file_id=file_id,
                file_uid=file_uid,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.CreateConversation,
                request=conversation_interface.CreateConversationRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateConversation,
            request=conversation_interface.CreateConversationRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListConversations,
                request=conversation_interface.ListConversationsRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListConversations,
            request=conversation_interface.ListConversationsRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.UpdateConversation,
                request=conversation_interface.UpdateConversationRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    new_conversation_id=new_conversation_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateConversation,
            request=conversation_interface.UpdateConversationRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                new_conversation_id=new_conversation_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.DeleteConversation,
                request=conversation_interface.DeleteConversationRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteConversation,
            request=conversation_interface.DeleteConversationRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.CreateMessage,
                request=conversation_interface.CreateMessageRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    content=content,
                    role=role,
                    type=conversation_interface.Message.MessageType.MESSAGE_TYPE_TEXT,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateMessage,
            request=conversation_interface.CreateMessageRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                content=content,
                role=role,
                type=conversation_interface.Message.MessageType.MESSAGE_TYPE_TEXT,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.ListMessages,
                request=conversation_interface.ListMessagesRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    latest_k=latest_k,
                    include_system_messages=include_system_messages,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListMessages,
            request=conversation_interface.ListMessagesRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                latest_k=latest_k,
                include_system_messages=include_system_messages,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.UpdateMessage,
                request=conversation_interface.UpdateMessageRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    message_uid=message_uid,
                    content=content,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateMessage,
            request=conversation_interface.UpdateMessageRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                message_uid=message_uid,
                content=content,
            ),
            metadata=self.host.metadata + self.metadata,
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
                method=self.host.async_client.DeleteMessage,
                request=conversation_interface.DeleteMessageRequest(
                    namespace_id=namespace_id,
                    catalog_id=catalog_id,
                    conversation_id=conversation_id,
                    message_uid=message_uid,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteMessage,
            request=conversation_interface.DeleteMessageRequest(
                namespace_id=namespace_id,
                catalog_id=catalog_id,
                conversation_id=conversation_id,
                message_uid=message_uid,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

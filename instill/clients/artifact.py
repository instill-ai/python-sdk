# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from datetime import datetime
from typing import Callable, List, Optional

# common
from google.protobuf import field_mask_pb2, timestamp_pb2

# artifact
import instill.protogen.artifact.artifact.v1alpha.artifact_pb2 as artifact_interface
import instill.protogen.artifact.artifact.v1alpha.artifact_public_service_pb2_grpc as artifact_service
import instill.protogen.artifact.artifact.v1alpha.chunk_pb2 as chunk_interface
import instill.protogen.artifact.artifact.v1alpha.file_pb2 as file_interface
import instill.protogen.artifact.artifact.v1alpha.knowledge_base_pb2 as knowledge_base_interface
import instill.protogen.artifact.artifact.v1alpha.object_pb2 as object_interface
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
from instill.clients.base import Client, RequestFactory
from instill.clients.instance import InstillInstance
from instill.helpers.const import HOST_URL_PROD
from instill.utils.error_handler import grpc_handler
from instill.utils.process_file import process_file


class ArtifactClient(Client):
    def __init__(
        self,
        api_token: str,
        lookup_func: Callable[[str], str],
        url: str = HOST_URL_PROD,
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
    def create_knowledge_base(
        self,
        namespace_id: str,
        knowledge_base_id: str = "",
        description: str = "",
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> knowledge_base_interface.CreateKnowledgeBaseResponse:
        tags = tags if tags is not None else []

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateKnowledgeBase,
                request=knowledge_base_interface.CreateKnowledgeBaseRequest(
                    namespace_id=namespace_id,
                    id=knowledge_base_id,
                    description=description,
                    tags=tags,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateKnowledgeBase,
            request=knowledge_base_interface.CreateKnowledgeBaseRequest(
                namespace_id=namespace_id,
                id=knowledge_base_id,
                description=description,
                tags=tags,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_knowledge_base(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        async_enabled: bool = False,
    ) -> knowledge_base_interface.GetKnowledgeBaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetKnowledgeBase,
                request=knowledge_base_interface.GetKnowledgeBaseRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetKnowledgeBase,
            request=knowledge_base_interface.GetKnowledgeBaseRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_knowledge_bases(
        self,
        namespace_id: str,
        page_size: int = 10,
        page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> knowledge_base_interface.ListKnowledgeBasesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListKnowledgeBases,
                request=knowledge_base_interface.ListKnowledgeBasesRequest(
                    namespace_id=namespace_id,
                    page_size=page_size,
                    page_token=page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListKnowledgeBases,
            request=knowledge_base_interface.ListKnowledgeBasesRequest(
                namespace_id=namespace_id,
                page_size=page_size,
                page_token=page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_knowledge_base(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        description: str = "",
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> knowledge_base_interface.UpdateKnowledgeBaseResponse:
        tags = tags if tags is not None else []

        # Create the knowledge base object with the fields to update
        kb = knowledge_base_interface.KnowledgeBase(
            description=description,
            tags=tags,
        )

        # Create update mask
        update_mask = field_mask_pb2.FieldMask(paths=["description", "tags"])

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateKnowledgeBase,
                request=knowledge_base_interface.UpdateKnowledgeBaseRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    knowledge_base=kb,
                    update_mask=update_mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateKnowledgeBase,
            request=knowledge_base_interface.UpdateKnowledgeBaseRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                knowledge_base=kb,
                update_mask=update_mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_knowledge_base(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        async_enabled: bool = False,
    ) -> knowledge_base_interface.DeleteKnowledgeBaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteKnowledgeBase,
                request=knowledge_base_interface.DeleteKnowledgeBaseRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteKnowledgeBase,
            request=knowledge_base_interface.DeleteKnowledgeBaseRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_file(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        file_path: str = "",
        file_data: Optional[file_interface.File] = None,
        async_enabled: bool = False,
    ) -> file_interface.CreateFileResponse:
        if file_data is None:
            file_data = process_file(file_path)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateFile,
                request=file_interface.CreateFileRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    file=file_data,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateFile,
            request=file_interface.CreateFileRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                file=file_data,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_file(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        file_id: str,
        view: Optional[file_interface.File.View] = None,
        async_enabled: bool = False,
    ) -> file_interface.GetFileResponse:
        if async_enabled:
            request = file_interface.GetFileRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                file_id=file_id,
            )
            if view is not None:
                request.view = view  # type: ignore[assignment]
            return RequestFactory(
                method=self.host.async_client.GetFile,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        request = file_interface.GetFileRequest(
            namespace_id=namespace_id,
            knowledge_base_id=knowledge_base_id,
            file_id=file_id,
        )
        if view is not None:
            request.view = view  # type: ignore[assignment]
        return RequestFactory(
            method=self.host.client.GetFile,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_files(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        page_size: int = 10,
        page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> file_interface.ListFilesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListFiles,
                request=file_interface.ListFilesRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    page_size=page_size,
                    page_token=page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListFiles,
            request=file_interface.ListFilesRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                page_size=page_size,
                page_token=page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_file(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        file_id: str,
        file_data: file_interface.File,
        update_mask: field_mask_pb2.FieldMask,
        async_enabled: bool = False,
    ) -> file_interface.UpdateFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateFile,
                request=file_interface.UpdateFileRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    file_id=file_id,
                    file=file_data,
                    update_mask=update_mask,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateFile,
            request=file_interface.UpdateFileRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                file_id=file_id,
                file=file_data,
                update_mask=update_mask,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_file(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        file_id: str,
        async_enabled: bool = False,
    ) -> file_interface.DeleteFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteFile,
                request=file_interface.DeleteFileRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    file_id=file_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteFile,
            request=file_interface.DeleteFileRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                file_id=file_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_chunk(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        file_id: str,
        chunk_id: str,
        async_enabled: bool = False,
    ) -> chunk_interface.GetChunkResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetChunk,
                request=chunk_interface.GetChunkRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    file_id=file_id,
                    chunk_id=chunk_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetChunk,
            request=chunk_interface.GetChunkRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                file_id=file_id,
                chunk_id=chunk_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_chunks(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        file_id: str,
        page_size: int = 100,
        page_token: str = "",
        filter_str: str = "",
        async_enabled: bool = False,
    ) -> chunk_interface.ListChunksResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListChunks,
                request=chunk_interface.ListChunksRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    file_id=file_id,
                    page_size=page_size,
                    page_token=page_token,
                    filter=filter_str,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListChunks,
            request=chunk_interface.ListChunksRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                file_id=file_id,
                page_size=page_size,
                page_token=page_token,
                filter=filter_str,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_chunk(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        chunk_id: str,
        retrievable: bool,
        async_enabled: bool = False,
    ) -> chunk_interface.UpdateChunkResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateChunk,
                request=chunk_interface.UpdateChunkRequest(
                    namespace_id=namespace_id,
                    knowledge_base_id=knowledge_base_id,
                    chunk_id=chunk_id,
                    retrievable=retrievable,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateChunk,
            request=chunk_interface.UpdateChunkRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                chunk_id=chunk_id,
                retrievable=retrievable,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def search_chunks(
        self,
        namespace_id: str,
        knowledge_base_id: str,
        text_prompt: str,
        top_k: int = 5,
        chunk_type: Optional[chunk_interface.Chunk.Type] = None,
        file_media_type: Optional[file_interface.File.FileMediaType] = None,
        file_ids: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        async_enabled: bool = False,
    ) -> chunk_interface.SearchChunksResponse:
        if async_enabled:
            request = chunk_interface.SearchChunksRequest(
                namespace_id=namespace_id,
                knowledge_base_id=knowledge_base_id,
                text_prompt=text_prompt,
                top_k=top_k,
            )
            if chunk_type is not None:
                request.type = chunk_type  # type: ignore[assignment]
            if file_media_type is not None:
                request.file_media_type = file_media_type
            if file_ids is not None:
                request.file_ids.extend(file_ids)
            if tags is not None:
                request.tags.extend(tags)
            return RequestFactory(
                method=self.host.async_client.SearchChunks,
                request=request,
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        request = chunk_interface.SearchChunksRequest(
            namespace_id=namespace_id,
            knowledge_base_id=knowledge_base_id,
            text_prompt=text_prompt,
            top_k=top_k,
        )
        if chunk_type is not None:
            request.type = chunk_type  # type: ignore[assignment]
        if file_media_type is not None:
            request.file_media_type = file_media_type
        if file_ids is not None:
            request.file_ids.extend(file_ids)
        if tags is not None:
            request.tags.extend(tags)
        return RequestFactory(
            method=self.host.client.SearchChunks,
            request=request,
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_object_upload_url(
        self,
        namespace_id: str,
        object_name: str,
        url_expire_days: int,
        last_modified_time: datetime,
        object_expire_days: int,
        async_enabled: bool = False,
    ) -> object_interface.GetObjectUploadURLResponse:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(last_modified_time)

        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetObjectUploadURL,
                request=object_interface.GetObjectUploadURLRequest(
                    namespace_id=namespace_id,
                    object_name=object_name,
                    url_expire_days=url_expire_days,
                    last_modified_time=timestamp,
                    object_expire_days=object_expire_days,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetObjectUploadURL,
            request=object_interface.GetObjectUploadURLRequest(
                namespace_id=namespace_id,
                object_name=object_name,
                url_expire_days=url_expire_days,
                last_modified_time=timestamp,
                object_expire_days=object_expire_days,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_object_download_url(
        self,
        namespace_id: str,
        object_uid: str,
        url_expire_days: int,
        async_enabled: bool = False,
    ) -> object_interface.GetObjectDownloadURLResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetObjectDownloadURL,
                request=object_interface.GetObjectDownloadURLRequest(
                    namespace_id=namespace_id,
                    object_uid=object_uid,
                    url_expire_days=url_expire_days,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetObjectDownloadURL,
            request=object_interface.GetObjectDownloadURLRequest(
                namespace_id=namespace_id,
                object_uid=object_uid,
                url_expire_days=url_expire_days,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

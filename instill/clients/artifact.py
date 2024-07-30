# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from typing import Dict

# artifact
import instill.protogen.artifact.artifact.v1alpha.artifact_pb2 as artifact_interface
import instill.protogen.artifact.artifact.v1alpha.artifact_public_service_pb2_grpc as artifact_service
import instill.protogen.artifact.artifact.v1alpha.chunk_pb2 as chunk_interface

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler


class ArtifactClient(Client):
    def __init__(self, async_enabled: bool) -> None:
        self.hosts: Dict[str, InstillInstance] = {}
        if DEFAULT_INSTANCE in global_config.hosts:
            self.instance = DEFAULT_INSTANCE
        elif len(global_config.hosts) == 0:
            self.instance = ""
        else:
            self.instance = list(global_config.hosts.keys())[0]

        if global_config.hosts is not None:
            for instance, config in global_config.hosts.items():
                self.hosts[instance] = InstillInstance(
                    artifact_service.ArtifactPublicServiceStub,
                    url=config.url,
                    token=config.token,
                    secure=config.secure,
                    async_enabled=async_enabled,
                )

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
    def create_knowledge_base(
        self,
        namespace_id: str,
        name: str,
        description: str,
        tags: list[str],
        async_enabled: bool = False,
    ) -> artifact_interface.CreateKnowledgeBaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.CreateKnowledgeBase,
                request=artifact_interface.CreateKnowledgeBaseRequest(
                    namespace_id=namespace_id,
                    name=name,
                    description=description,
                    tags=tags,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateKnowledgeBase,
            request=artifact_interface.CreateKnowledgeBaseRequest(
                namespace_id=namespace_id,
                name=name,
                description=description,
                tags=tags,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_knowledge_bases(
        self,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.ListKnowledgeBasesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListKnowledgeBases,
                request=artifact_interface.ListKnowledgeBasesRequest(
                    namespace_id=namespace_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListKnowledgeBases,
            request=artifact_interface.ListKnowledgeBasesRequest(
                namespace_id=namespace_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_knowledge_base(
        self,
        kb_id: str,
        description: str,
        tags: str,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.UpdateKnowledgeBaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateKnowledgeBase,
                request=artifact_interface.UpdateKnowledgeBaseRequest(
                    kb_id=kb_id,
                    description=description,
                    tags=tags,
                    namespace_id=namespace_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateKnowledgeBase,
            request=artifact_interface.UpdateKnowledgeBaseRequest(
                kb_id=kb_id,
                description=description,
                tags=tags,
                namespace_id=namespace_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_knowledge_base(
        self,
        namespace_id: str,
        kb_id: str,
        async_enabled: bool = False,
    ) -> artifact_interface.DeleteKnowledgeBaseResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteKnowledgeBase,
                request=artifact_interface.DeleteKnowledgeBaseRequest(
                    namespace_id=namespace_id,
                    kb_id=kb_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteKnowledgeBase,
            request=artifact_interface.DeleteKnowledgeBaseRequest(
                namespace_id=namespace_id,
                kb_id=kb_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def upload_knowledge_base_file(
        self,
        namespace_id: str,
        kb_id: str,
        file: artifact_interface.File,
        async_enabled: bool = False,
    ) -> artifact_interface.UploadKnowledgeBaseFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UploadKnowledgeBaseFile,
                request=artifact_interface.UploadKnowledgeBaseFileRequest(
                    namespace_id=namespace_id,
                    kb_id=kb_id,
                    file=file,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UploadKnowledgeBaseFile,
            request=artifact_interface.UploadKnowledgeBaseFileRequest(
                namespace_id=namespace_id,
                kb_id=kb_id,
                file=file,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def delete_knowledge_base_file(
        self,
        file_uid: str,
        async_enabled: bool = False,
    ) -> artifact_interface.DeleteKnowledgeBaseFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteKnowledgeBaseFile,
                request=artifact_interface.DeleteKnowledgeBaseFileRequest(
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteKnowledgeBaseFile,
            request=artifact_interface.DeleteKnowledgeBaseFileRequest(
                file_uid=file_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def process_knowledge_base_files(
        self,
        file_uids: list[str],
        async_enabled: bool = False,
    ) -> artifact_interface.ProcessKnowledgeBaseFilesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ProcessKnowledgeBaseFiles,
                request=artifact_interface.ProcessKnowledgeBaseFilesRequest(
                    file_uids=file_uids,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ProcessKnowledgeBaseFiles,
            request=artifact_interface.ProcessKnowledgeBaseFilesRequest(
                file_uids=file_uids,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_knowledge_base_files(
        self,
        namespace_id: str,
        kb_id: str,
        page_size: int,
        page_token: str,
        files_filter: artifact_interface.ListKnowledgeBaseFilesFilter,
        async_enabled: bool = False,
    ) -> artifact_interface.ListKnowledgeBaseFilesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListKnowledgeBaseFiles,
                request=artifact_interface.ListKnowledgeBaseFilesRequest(
                    namespace_id=namespace_id,
                    kb_id=kb_id,
                    page_size=page_size,
                    page_token=page_token,
                    filter=files_filter,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListKnowledgeBaseFiles,
            request=artifact_interface.ListKnowledgeBaseFilesRequest(
                namespace_id=namespace_id,
                kb_id=kb_id,
                page_size=page_size,
                page_token=page_token,
                filter=files_filter,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_chunks(
        self,
        namespace_id: str,
        kb_id: str,
        file_uid: str,
        async_enabled: bool = False,
    ) -> chunk_interface.ListChunksResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListChunks,
                request=chunk_interface.ListChunksRequest(
                    namespace_id=namespace_id,
                    kb_id=kb_id,
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListChunks,
            request=chunk_interface.ListChunksRequest(
                namespace_id=namespace_id,
                kb_id=kb_id,
                file_uid=file_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def get_source_file(
        self,
        namespace_id: str,
        kb_id: str,
        file_uid: str,
        async_enabled: bool = False,
    ) -> chunk_interface.GetSourceFileResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.GetSourceFile,
                request=chunk_interface.GetSourceFileRequest(
                    namespace_id=namespace_id,
                    kb_id=kb_id,
                    file_uid=file_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetSourceFile,
            request=chunk_interface.GetSourceFileRequest(
                namespace_id=namespace_id,
                kb_id=kb_id,
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
        kb_id: str,
        text_prompt: str,
        topk: int,
        async_enabled: bool = False,
    ) -> chunk_interface.SimilarityChunksSearchResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.SimilarityChunksSearch,
                request=chunk_interface.SimilarityChunksSearchRequest(
                    namespace_id=namespace_id,
                    kb_id=kb_id,
                    text_prompt=text_prompt,
                    topk=topk,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.SimilarityChunksSearch,
            request=chunk_interface.SimilarityChunksSearchRequest(
                namespace_id=namespace_id,
                kb_id=kb_id,
                text_prompt=text_prompt,
                topk=topk,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

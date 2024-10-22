# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from typing import Callable, List

# app
import instill.protogen.app.app.v1alpha.app_pb2 as app_interface
import instill.protogen.app.app.v1alpha.app_public_service_pb2_grpc as app_service
import instill.protogen.app.app.v1alpha.conversation_pb2 as conversation_interface

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
from instill.clients.base import Client, RequestFactory
from instill.clients.instance import InstillInstance
from instill.helpers.const import HOST_URL_PROD
from instill.utils.error_handler import grpc_handler


class AppClient(Client):
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
            app_service.AppPublicServiceStub,
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
    ) -> app_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Liveness,
                request=app_interface.LivenessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Liveness,
            request=app_interface.LivenessRequest(),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    def readiness(
        self,
        async_enabled: bool = False,
    ) -> app_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Readiness,
                request=app_interface.ReadinessRequest(),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Readiness,
            request=app_interface.ReadinessRequest(),
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
    def create_app(
        self,
        namespace_id: str,
        app_id: str,
        description: str,
        tags: list[str],
        async_enabled: bool = False,
    ) -> app_interface.CreateAppResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateApp,
                request=app_interface.CreateAppRequest(
                    namespace_id=namespace_id,
                    id=app_id,
                    description=description,
                    tags=tags,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateApp,
            request=app_interface.CreateAppRequest(
                namespace_id=namespace_id,
                id=app_id,
                description=description,
                tags=tags,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_apps(
        self,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> app_interface.ListAppsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListApps,
                request=app_interface.ListAppsRequest(
                    namespace_id=namespace_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListApps,
            request=app_interface.ListAppsRequest(
                namespace_id=namespace_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_app(
        self,
        namespace_id: str,
        app_id: str,
        new_app_id: str,
        new_description: str,
        new_tags: list[str],
        last_ai_assistant_app_catalog_uid: str,
        last_ai_assistant_app_top_k: int,
        async_enabled: bool = False,
    ) -> app_interface.UpdateAppResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateApp,
                request=app_interface.UpdateAppRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    new_app_id=new_app_id,
                    new_description=new_description,
                    new_tags=new_tags,
                    last_ai_assistant_app_catalog_uid=last_ai_assistant_app_catalog_uid,
                    last_ai_assistant_app_top_k=last_ai_assistant_app_top_k,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateApp,
            request=app_interface.UpdateAppRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                new_app_id=new_app_id,
                new_description=new_description,
                new_tags=new_tags,
                last_ai_assistant_app_catalog_uid=last_ai_assistant_app_catalog_uid,
                last_ai_assistant_app_top_k=last_ai_assistant_app_top_k,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_app(
        self,
        namespace_id: str,
        app_id: str,
        async_enabled: bool = False,
    ) -> app_interface.DeleteAppResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteApp,
                request=app_interface.DeleteAppRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteApp,
            request=app_interface.DeleteAppRequest(
                namespace_id=namespace_id,
                app_id=app_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_conversation(
        self,
        namespace_id: str,
        app_id: str,
        conversation_id: str,
        async_enabled: bool = False,
    ) -> conversation_interface.CreateConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.CreateConversation,
                request=conversation_interface.CreateConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.CreateConversation,
            request=conversation_interface.CreateConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def list_conversations(
        self,
        namespace_id: str,
        app_id: str,
        conversation_uid: str,
        conversation_id: str,
        page_size: int = 10,
        page_token: str = "",
        if_all: bool = False,
        async_enabled: bool = False,
    ) -> conversation_interface.ListConversationsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListConversations,
                request=conversation_interface.ListConversationsRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_uid=conversation_uid,
                    conversation_id=conversation_id,
                    page_size=page_size,
                    page_token=page_token,
                    if_all=if_all,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListConversations,
            request=conversation_interface.ListConversationsRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_uid=conversation_uid,
                conversation_id=conversation_id,
                page_size=page_size,
                page_token=page_token,
                if_all=if_all,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_conversation(
        self,
        namespace_id: str,
        app_id: str,
        conversation_id: str,
        new_conversation_id: str,
        last_used_catalog_uid: str,
        last_used_top_k: int,
        async_enabled: bool = False,
    ) -> conversation_interface.UpdateConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.UpdateConversation,
                request=conversation_interface.UpdateConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                    new_conversation_id=new_conversation_id,
                    last_used_catalog_uid=last_used_catalog_uid,
                    last_used_top_k=last_used_top_k,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.UpdateConversation,
            request=conversation_interface.UpdateConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
                new_conversation_id=new_conversation_id,
                last_used_catalog_uid=last_used_catalog_uid,
                last_used_top_k=last_used_top_k,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def delete_conversation(
        self,
        namespace_id: str,
        app_id: str,
        conversation_id: str,
        async_enabled: bool = False,
    ) -> conversation_interface.DeleteConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteConversation,
                request=conversation_interface.DeleteConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteConversation,
            request=conversation_interface.DeleteConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def create_message(
        self,
        namespace_id: str,
        app_id: str,
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
                    app_id=app_id,
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
                app_id=app_id,
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
        app_id: str,
        conversation_id: str,
        latest_k: int,
        include_system_messages: bool,
        message_uid: str,
        page_size: int = 10,
        page_token: str = "",
        if_all: bool = False,
        async_enabled: bool = False,
    ) -> conversation_interface.ListMessagesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.ListMessages,
                request=conversation_interface.ListMessagesRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                    latest_k=latest_k,
                    include_system_messages=include_system_messages,
                    message_uid=message_uid,
                    page_size=page_size,
                    page_token=page_token,
                    if_all=if_all,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.ListMessages,
            request=conversation_interface.ListMessagesRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
                latest_k=latest_k,
                include_system_messages=include_system_messages,
                message_uid=message_uid,
                page_size=page_size,
                page_token=page_token,
                if_all=if_all,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def update_message(
        self,
        namespace_id: str,
        app_id: str,
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
                    app_id=app_id,
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
                app_id=app_id,
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
        app_id: str,
        conversation_id: str,
        message_uid: str,
        async_enabled: bool = False,
    ) -> conversation_interface.DeleteMessageResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.DeleteMessage,
                request=conversation_interface.DeleteMessageRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                    message_uid=message_uid,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.DeleteMessage,
            request=conversation_interface.DeleteMessageRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
                message_uid=message_uid,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def get_playground_conversation(
        self,
        namespace_id: str,
        app_id: str,
        async_enabled: bool = False,
    ) -> app_interface.GetPlaygroundConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.GetPlaygroundConversation,
                request=app_interface.GetPlaygroundConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.GetPlaygroundConversation,
            request=app_interface.GetPlaygroundConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def restart_playground_conversation(
        self,
        namespace_id: str,
        app_id: str,
        async_enabled: bool = False,
    ) -> app_interface.RestartPlaygroundConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.RestartPlaygroundConversation,
                request=app_interface.RestartPlaygroundConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.RestartPlaygroundConversation,
            request=app_interface.RestartPlaygroundConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

    @grpc_handler
    def chat(
        self,
        namespace_id: str,
        app_id: str,
        catalog_id: str,
        conversation_uid: str,
        message: str,
        top_k: int,
        async_enabled: bool = False,
    ) -> conversation_interface.ChatResponse:
        if async_enabled:
            return RequestFactory(
                method=self.host.async_client.Chat,
                request=conversation_interface.ChatRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    catalog_id=catalog_id,
                    conversation_uid=conversation_uid,
                    message=message,
                    top_k=top_k,
                ),
                metadata=self.host.metadata + self.metadata,
            ).send_async()

        return RequestFactory(
            method=self.host.client.Chat,
            request=conversation_interface.ChatRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                catalog_id=catalog_id,
                conversation_uid=conversation_uid,
                message=message,
                top_k=top_k,
            ),
            metadata=self.host.metadata + self.metadata,
        ).send_sync()

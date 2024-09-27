# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
from typing import Dict

# app
import instill.protogen.app.app.v1alpha.app_pb2 as app_interface
import instill.protogen.app.app.v1alpha.app_public_service_pb2_grpc as app_service
import instill.protogen.app.app.v1alpha.conversation_pb2 as conversation_interface

# common
import instill.protogen.common.healthcheck.v1beta.healthcheck_pb2 as healthcheck
from instill.clients.base import Client, RequestFactory
from instill.clients.constant import DEFAULT_INSTANCE
from instill.clients.instance import InstillInstance
from instill.configuration import global_config
from instill.utils.error_handler import grpc_handler


class AppClient(Client):
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
                    app_service.AppPublicServiceStub,
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

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: str):
        self._metadata = metadata

    @grpc_handler
    def liveness(
        self,
        async_enabled: bool = False,
    ) -> app_interface.LivenessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Liveness,
                request=app_interface.LivenessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Liveness,
            request=app_interface.LivenessRequest(),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def readiness(
        self,
        async_enabled: bool = False,
    ) -> app_interface.ReadinessResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Readiness,
                request=app_interface.ReadinessRequest(),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Readiness,
            request=app_interface.ReadinessRequest(),
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
                method=self.hosts[self.instance].async_client.CreateApp,
                request=app_interface.CreateAppRequest(
                    namespace_id=namespace_id,
                    id=app_id,
                    description=description,
                    tags=tags,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateApp,
            request=app_interface.CreateAppRequest(
                namespace_id=namespace_id,
                id=app_id,
                description=description,
                tags=tags,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_apps(
        self,
        namespace_id: str,
        async_enabled: bool = False,
    ) -> app_interface.ListAppsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListApps,
                request=app_interface.ListAppsRequest(
                    namespace_id=namespace_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListApps,
            request=app_interface.ListAppsRequest(
                namespace_id=namespace_id,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.UpdateApp,
                request=app_interface.UpdateAppRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    new_app_id=new_app_id,
                    new_description=new_description,
                    new_tags=new_tags,
                    last_ai_assistant_app_catalog_uid=last_ai_assistant_app_catalog_uid,
                    last_ai_assistant_app_top_k=last_ai_assistant_app_top_k,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateApp,
            request=app_interface.UpdateAppRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                new_app_id=new_app_id,
                new_description=new_description,
                new_tags=new_tags,
                last_ai_assistant_app_catalog_uid=last_ai_assistant_app_catalog_uid,
                last_ai_assistant_app_top_k=last_ai_assistant_app_top_k,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.DeleteApp,
                request=app_interface.DeleteAppRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteApp,
            request=app_interface.DeleteAppRequest(
                namespace_id=namespace_id,
                app_id=app_id,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.CreateConversation,
                request=conversation_interface.CreateConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.CreateConversation,
            request=conversation_interface.CreateConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def list_conversations(
        self,
        namespace_id: str,
        app_id: str,
        conversation_uid: str,
        conversation_id: str,
        if_all: bool,
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> conversation_interface.ListConversationsResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListConversations,
                request=conversation_interface.ListConversationsRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_uid=conversation_uid,
                    conversation_id=conversation_id,
                    if_all=if_all,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListConversations,
            request=conversation_interface.ListConversationsRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_uid=conversation_uid,
                conversation_id=conversation_id,
                if_all=if_all,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_conversation(
        self,
        namespace_id: str,
        app_id: str,
        conversation_id: str,
        new_conversation_id: str,
        async_enabled: bool = False,
    ) -> conversation_interface.UpdateConversationResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.UpdateConversation,
                request=conversation_interface.UpdateConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                    new_conversation_id=new_conversation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateConversation,
            request=conversation_interface.UpdateConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
                new_conversation_id=new_conversation_id,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.DeleteConversation,
                request=conversation_interface.DeleteConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteConversation,
            request=conversation_interface.DeleteConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.CreateMessage,
                request=conversation_interface.CreateMessageRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
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
                app_id=app_id,
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
        app_id: str,
        conversation_id: str,
        latest_k: int,
        include_system_messages: bool,
        if_all: bool,
        message_uid: str,
        page_size: int = 10,
        page_token: str = "",
        async_enabled: bool = False,
    ) -> conversation_interface.ListMessagesResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.ListMessages,
                request=conversation_interface.ListMessagesRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                    latest_k=latest_k,
                    include_system_messages=include_system_messages,
                    if_all=if_all,
                    message_uid=message_uid,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.ListMessages,
            request=conversation_interface.ListMessagesRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
                latest_k=latest_k,
                include_system_messages=include_system_messages,
                if_all=if_all,
                message_uid=message_uid,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.UpdateMessage,
                request=conversation_interface.UpdateMessageRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
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
                app_id=app_id,
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
        app_id: str,
        conversation_id: str,
        message_uid: str,
        async_enabled: bool = False,
    ) -> conversation_interface.DeleteMessageResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.DeleteMessage,
                request=conversation_interface.DeleteMessageRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    conversation_id=conversation_id,
                    message_uid=message_uid,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.DeleteMessage,
            request=conversation_interface.DeleteMessageRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                conversation_id=conversation_id,
                message_uid=message_uid,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def update_ai_assistant_app_playground(
        self,
        namespace_id: str,
        app_id: str,
        last_ai_app_catalog_uid: str,
        last_ai_app_top_k: int,
        async_enabled: bool = False,
    ) -> app_interface.UpdateAIAssistantAppPlaygroundResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[
                    self.instance
                ].async_client.UpdateAIAssistantAppPlayground,
                request=app_interface.UpdateAIAssistantAppPlaygroundRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    last_ai_app_catalog_uid=last_ai_app_catalog_uid,
                    last_ai_app_top_k=last_ai_app_top_k,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.UpdateAIAssistantAppPlayground,
            request=app_interface.UpdateAIAssistantAppPlaygroundRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                last_ai_app_catalog_uid=last_ai_app_catalog_uid,
                last_ai_app_top_k=last_ai_app_top_k,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[self.instance].async_client.GetPlaygroundConversation,
                request=app_interface.GetPlaygroundConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.GetPlaygroundConversation,
            request=app_interface.GetPlaygroundConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
            ),
            metadata=self.hosts[self.instance].metadata,
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
                method=self.hosts[
                    self.instance
                ].async_client.RestartPlaygroundConversation,
                request=app_interface.RestartPlaygroundConversationRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.RestartPlaygroundConversation,
            request=app_interface.RestartPlaygroundConversationRequest(
                namespace_id=namespace_id,
                app_id=app_id,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

    @grpc_handler
    def chat(
        self,
        namespace_id: str,
        app_id: str,
        catalog_id: str,
        conversation_uid: str,
        message: str,
        async_enabled: bool = False,
    ) -> conversation_interface.ChatResponse:
        if async_enabled:
            return RequestFactory(
                method=self.hosts[self.instance].async_client.Chat,
                request=conversation_interface.ChatRequest(
                    namespace_id=namespace_id,
                    app_id=app_id,
                    catalog_id=catalog_id,
                    conversation_uid=conversation_uid,
                    message=message,
                ),
                metadata=self.hosts[self.instance].metadata,
            ).send_async()

        return RequestFactory(
            method=self.hosts[self.instance].client.Chat,
            request=conversation_interface.ChatRequest(
                namespace_id=namespace_id,
                app_id=app_id,
                catalog_id=catalog_id,
                conversation_uid=conversation_uid,
                message=message,
            ),
            metadata=self.hosts[self.instance].metadata,
        ).send_sync()

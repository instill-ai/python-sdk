# pylint: disable=no-name-in-module
from instill.clients.artifact import ArtifactClient
from instill.clients.mgmt import MgmtClient
from instill.clients.model import ModelClient
from instill.clients.pipeline import PipelineClient
from instill.utils.error_handler import NotServingException
from instill.utils.logger import Logger


class InstillClient:
    def __init__(self, api_token: str = "", async_enabled: bool = False) -> None:
        self.mgmt_service = MgmtClient(api_token=api_token, async_enabled=async_enabled)
        if not self.mgmt_service.is_serving():
            Logger.w("Instill Core is required")
            raise NotServingException

        user_name = self.mgmt_service.get_user().user.name

        self.pipeline_service = PipelineClient(
            namespace=user_name,
            async_enabled=async_enabled,
            api_token=api_token,
        )
        if not self.pipeline_service.is_serving():
            Logger.w("Instill VDP is not serving, VDP functionalities will not work")

        self.model_service = ModelClient(
            namespace=user_name,
            async_enabled=async_enabled,
            api_token=api_token,
        )
        if not self.model_service.is_serving():
            Logger.w(
                "Instill Model is not serving, Model functionalities will not work"
            )

        self.artifact_service = ArtifactClient(
            async_enabled=async_enabled, api_token=api_token
        )
        if not self.artifact_service.is_serving():
            Logger.w(
                "Instill Artifact is not serving, Artifact functionalities will not work"
            )

    def set_instance(self, instance: str):
        self.mgmt_service.instance = instance
        self.pipeline_service.instance = instance
        self.model_service.instance = instance
        self.artifact_service.instance = instance

    def close(self):
        self.mgmt_service.close()
        self.pipeline_service.close()
        self.model_service.close()
        self.artifact_service.close()

    async def async_close(self):
        self.mgmt_service.async_close()
        self.pipeline_service.async_close()
        self.model_service.async_close()
        self.artifact_service.async_close()

    def get_artifact(self) -> ArtifactClient:
        return self.artifact_service

    def get_pipeline(self) -> PipelineClient:
        return self.pipeline_service

    def get_model(self) -> ModelClient:
        return self.model_service


def get_client(async_enabled: bool = False) -> InstillClient:
    return InstillClient(async_enabled=async_enabled)


def init_core_client(api_token: str = "", async_enabled: bool = False) -> InstillClient:
    return InstillClient(api_token=api_token, async_enabled=async_enabled)


def init_artifact_client(
    api_token: str = "", async_enabled: bool = False
) -> ArtifactClient:
    client = ArtifactClient(api_token=api_token, async_enabled=async_enabled)
    if not client.is_serving():
        Logger.w(
            "Instill Artifact is not serving, Artifact functionalities will not work"
        )
        raise NotServingException

    return client


def init_model_client(api_token: str = "", async_enabled: bool = False) -> ModelClient:
    mgmt_service = MgmtClient(api_token=api_token, async_enabled=False)
    if not mgmt_service.is_serving():
        Logger.w("Instill Core is required")
        raise NotServingException

    user_name = mgmt_service.get_user().user.name
    mgmt_service.close()

    client = ModelClient(
        namespace=user_name, api_token=api_token, async_enabled=async_enabled
    )
    if not client.is_serving():
        Logger.w("Instill Model is not serving, Model functionalities will not work")
        raise NotServingException

    return client


def init_pipeline_client(
    namespace: str = "", api_token: str = "", async_enabled: bool = False
) -> PipelineClient:
    if namespace == "":
        mgmt_service = MgmtClient(api_token=api_token, async_enabled=False)
        if not mgmt_service.is_serving():
            Logger.w("Instill Core is required")
            raise NotServingException

        namespace = mgmt_service.get_user().user.name
        mgmt_service.close()
    else:
        namespace = f"organizations/{namespace}"

    client = PipelineClient(
        namespace=namespace, api_token=api_token, async_enabled=async_enabled
    )
    if not client.is_serving():
        Logger.w("Instill VDP is not serving, VDP functionalities will not work")
        raise NotServingException

    return client


def init_mgmt_client(api_token: str = "", async_enabled: bool = False) -> MgmtClient:
    client = MgmtClient(api_token=api_token, async_enabled=async_enabled)
    if not client.is_serving():
        Logger.w("Instill Core is required")
        raise NotServingException

    return client

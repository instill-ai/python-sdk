# pylint: disable=no-name-in-module,no-member
import instill.protogen.core.mgmt.v1beta.mgmt_pb2 as mgmt_interface
from instill.clients.app import AppClient
from instill.clients.artifact import ArtifactClient
from instill.clients.mgmt import MgmtClient
from instill.clients.model import ModelClient
from instill.clients.pipeline import PipelineClient
from instill.helpers.const import HOST_URL_PROD
from instill.utils.error_handler import NotServingException
from instill.utils.logger import Logger


class InstillClient:
    def __init__(
        self,
        api_token: str,
        url: str = HOST_URL_PROD,
        secure: bool = True,
        requester_id="",
        async_enabled: bool = False,
    ) -> None:
        self.mgmt = MgmtClient(
            api_token=api_token,
            url=url,
            secure=secure,
            requester_id=requester_id,
            async_enabled=async_enabled,
        )
        if not self.mgmt.is_serving():
            Logger.w("Instill Core is required")
            raise NotServingException

        self.pipeline = PipelineClient(
            api_token=api_token,
            url=url,
            secure=secure,
            lookup_func=self._lookup_namespace_uid,
            requester_id=requester_id,
            async_enabled=async_enabled,
        )
        if not self.pipeline.is_serving():
            Logger.w("Instill VDP is not serving, VDP functionalities will not work")

        self.model = ModelClient(
            api_token=api_token,
            url=url,
            secure=secure,
            lookup_func=self._lookup_namespace_uid,
            requester_id=requester_id,
            async_enabled=async_enabled,
        )
        if not self.model.is_serving():
            Logger.w(
                "Instill Model is not serving, Model functionalities will not work"
            )

        self.artifact = ArtifactClient(
            api_token=api_token,
            url=url,
            secure=secure,
            lookup_func=self._lookup_namespace_uid,
            requester_id=requester_id,
            async_enabled=async_enabled,
        )
        if not self.artifact.is_serving():
            Logger.w(
                "Instill Artifact is not serving, Artifact functionalities will not work"
            )

        self.app = AppClient(
            api_token=api_token,
            url=url,
            secure=secure,
            lookup_func=self._lookup_namespace_uid,
            requester_id=requester_id,
            async_enabled=async_enabled,
        )
        if not self.app.is_serving():
            Logger.w("Instill App is not serving, App functionalities will not work")

    def _lookup_namespace_uid(self, namespace_id: str):
        resp = self.mgmt.check_namespace(namespace_id)
        if resp.type == mgmt_interface.CheckNamespaceAdminResponse.NAMESPACE_USER:
            namespace_uid = self.mgmt.get_user(namespace_id).user.uid
        elif (
            resp.type
            == mgmt_interface.CheckNamespaceAdminResponse.NAMESPACE_ORGANIZATION
        ):
            namespace_uid = self.mgmt.get_organization(namespace_id).organization.uid
        else:
            raise Exception("namespace ID not available")

        return namespace_uid

    def close(self):
        self.mgmt.close()
        self.pipeline.close()
        self.model.close()
        self.artifact.close()
        self.app.close()

    async def async_close(self):
        self.mgmt.async_close()
        self.pipeline.async_close()
        self.model.async_close()
        self.artifact.async_close()
        self.app.async_close()

    def get_mgmt(self) -> MgmtClient:
        return self.mgmt

    def get_artifact(self) -> ArtifactClient:
        return self.artifact

    def get_pipeline(self) -> PipelineClient:
        return self.pipeline

    def get_model(self) -> ModelClient:
        return self.model

    def get_app(self) -> AppClient:
        return self.app


def init_core_client(
    api_token: str,
    requester_id="",
    url: str = HOST_URL_PROD,
    async_enabled: bool = False,
) -> InstillClient:
    return InstillClient(
        api_token=api_token,
        requester_id=requester_id,
        url=url,
        async_enabled=async_enabled,
    )


def init_artifact_client(
    api_token: str,
    requester_id: str = "",
    url: str = HOST_URL_PROD,
    async_enabled: bool = False,
) -> ArtifactClient:
    client = InstillClient(
        api_token=api_token,
        requester_id=requester_id,
        url=url,
        async_enabled=async_enabled,
    )
    if not client.get_artifact().is_serving():
        Logger.w(
            "Instill Artifact is not serving, Artifact functionalities will not work"
        )
        raise NotServingException

    return client.get_artifact()


def init_model_client(
    api_token: str,
    requester_id="",
    url: str = HOST_URL_PROD,
    async_enabled: bool = False,
) -> ModelClient:
    client = InstillClient(
        api_token=api_token,
        requester_id=requester_id,
        url=url,
        async_enabled=async_enabled,
    )
    if not client.get_model().is_serving():
        Logger.w("Instill Model is not serving, Model functionalities will not work")
        raise NotServingException

    return client.get_model()


def init_pipeline_client(
    api_token: str,
    requester_id="",
    url: str = HOST_URL_PROD,
    async_enabled: bool = False,
) -> PipelineClient:
    client = InstillClient(
        api_token=api_token,
        requester_id=requester_id,
        url=url,
        async_enabled=async_enabled,
    )
    if not client.get_pipeline().is_serving():
        Logger.w("Instill VDP is not serving, VDP functionalities will not work")
        raise NotServingException

    return client.get_pipeline()


def init_mgmt_client(
    api_token: str,
    requester_id="",
    url: str = HOST_URL_PROD,
    async_enabled: bool = False,
) -> MgmtClient:
    client = InstillClient(
        api_token=api_token,
        requester_id=requester_id,
        url=url,
        async_enabled=async_enabled,
    )
    if not client.get_mgmt().is_serving():
        Logger.w("Instill Core is required")
        raise NotServingException

    return client.get_mgmt()


def init_app_client(
    api_token: str = "",
    requester_id: str = "",
    url: str = HOST_URL_PROD,
    async_enabled: bool = False,
) -> AppClient:
    client = InstillClient(
        api_token=api_token,
        requester_id=requester_id,
        url=url,
        async_enabled=async_enabled,
    )
    if not client.get_app().is_serving():
        Logger.w("Instill App is not serving, App functionalities will not work")
        raise NotServingException

    return client.get_app()

# pylint: disable=no-name-in-module
from instill.clients.connector import ConnectorClient
from instill.clients.mgmt import MgmtClient
from instill.clients.model import ModelClient
from instill.clients.pipeline import PipelineClient
from instill.utils.error_handler import NotServingException
from instill.utils.logger import Logger

_mgmt_client = None
_connector_client = None
_pipeline_client = None
_model_client = None
_client = None


def _get_mgmt_client() -> MgmtClient:
    global _mgmt_client

    if _mgmt_client is None:
        _mgmt_client = MgmtClient()

    return _mgmt_client


def _get_connector_client() -> ConnectorClient:
    global _connector_client

    if _connector_client is None:
        _connector_client = ConnectorClient(
            namespace=_get_mgmt_client().get_user().name
        )

    return _connector_client


def _get_pipeline_client() -> PipelineClient:
    global _pipeline_client

    if _pipeline_client is None:
        _pipeline_client = PipelineClient(namespace=_get_mgmt_client().get_user().name)

    return _pipeline_client


def _get_model_client() -> ModelClient:
    global _model_client

    if _model_client is None:
        _model_client = ModelClient(namespace=_get_mgmt_client().get_user().name)

    return _model_client


class InstillClient:
    def __init__(self) -> None:
        self.mgmt_service = _get_mgmt_client()
        if not self.mgmt_service.is_serving():
            Logger.w("Instill Base is required")
            raise NotServingException
        self.connector_service = _get_connector_client()
        self.pipeline_service = _get_pipeline_client()
        if (
            not self.connector_service.is_serving()
            and not self.pipeline_service.is_serving()
        ):
            Logger.w("Instill VDP is not serving, VDP functionalities will not work")
        self.model_service = _get_model_client()
        if not self.model_service.is_serving():
            Logger.w(
                "Instill Model is not serving, Model functionalities will not work"
            )

    def set_instance(self, instance: str):
        self.mgmt_service.instance = instance
        self.connector_service.instance = instance
        self.pipeline_service.instance = instance
        self.model_service.instance = instance


def get_client() -> InstillClient:
    global _client

    if _client is None:
        _client = InstillClient()

    return _client

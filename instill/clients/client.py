# pylint: disable=no-name-in-module
from instill.clients.connector import ConnectorClient
from instill.clients.mgmt import MgmtClient
from instill.clients.model import ModelClient
from instill.clients.pipeline import PipelineClient

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


def _get_connector_clinet() -> ConnectorClient:
    global _connector_client

    if _connector_client is None:
        _connector_client = ConnectorClient(
            namespace=_get_mgmt_client().get_user().name
        )

    return _connector_client


def _get_pipeline_clinet() -> PipelineClient:
    global _pipeline_client

    if _pipeline_client is None:
        _pipeline_client = PipelineClient(namespace=_get_mgmt_client().get_user().name)

    return _pipeline_client


def _get_model_clinet() -> ModelClient:
    global _model_client

    if _model_client is None:
        _model_client = ModelClient(namespace=_get_mgmt_client().get_user().name)

    return _model_client


class InstillClient:
    def __init__(self) -> None:
        self.mgmt_service = _get_mgmt_client()
        self.connector_service = _get_connector_clinet()
        self.pipeline_service = _get_pipeline_clinet()
        self.model_serevice = _get_model_clinet()

    def set_instance(self, instance: str):
        self.mgmt_service.instance = instance
        self.connector_service.instance = instance
        self.pipeline_service.instance = instance
        self.model_serevice.instance = instance


def get_client() -> InstillClient:
    global _client

    if _client is None:
        _client = InstillClient()

    return _client

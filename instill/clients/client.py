# pylint: disable=no-name-in-module
from instill.clients.mgmt import MgmtClient
from instill.clients.model import ModelClient
from instill.clients.pipeline import PipelineClient
from instill.utils.error_handler import NotServingException
from instill.utils.logger import Logger


class InstillClient:
    def __init__(self) -> None:
        self.mgmt_service = MgmtClient()
        if not self.mgmt_service.is_serving():
            Logger.w("Instill Core is required")
            raise NotServingException
        self.pipeline_service = PipelineClient(
            namespace=self.mgmt_service.get_user().name
        )
        if not self.pipeline_service.is_serving():
            Logger.w("Instill VDP is not serving, VDP functionalities will not work")
        self.model_service = ModelClient(namespace=self.mgmt_service.get_user().name)
        if not self.model_service.is_serving():
            Logger.w(
                "Instill Model is not serving, Model functionalities will not work"
            )

    def set_instance(self, instance: str):
        self.mgmt_service.instance = instance
        self.pipeline_service.instance = instance
        self.model_service.instance = instance

    def close(self):
        if self.mgmt_service.is_serving():
            for host in self.mgmt_service.hosts.values():
                host.channel.close()
                host.async_channel.close()
        if self.pipeline_service.is_serving():
            for host in self.pipeline_service.hosts.values():
                host.channel.close()
                host.async_channel.close()
        if self.model_service.is_serving():
            for host in self.model_service.hosts.values():
                host.channel.close()
                host.async_channel.close()


def get_client() -> InstillClient:
    return InstillClient()

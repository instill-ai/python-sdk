# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Union
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_interface
from instill.resources.errors import ComponentTypeExection


class Component:
    def __init__(
        self,
        name: str,
        component_type: str,
        component: Union[
            pipeline_interface.ConnectorComponent,
            pipeline_interface.OperatorComponent,
            pipeline_interface.IteratorComponent,
        ],
    ):
        c = pipeline_interface.Component()
        c.id = name

        if component_type == "connector":
            c.connector_component = component
        elif component_type == "operator":
            c.operator_component = component
        elif component_type == "iterator":
            c.iterator_component = component
        else:
            raise ComponentTypeExection

        self.c = c

    def get_component(self) -> pipeline_interface.Component:
        return self.c

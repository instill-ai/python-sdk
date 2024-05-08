# pylint: disable=no-member,wrong-import-position,no-name-in-module
from typing import Union

from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import Component as Comp
from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import (
    ConnectorComponent,
    IteratorComponent,
    OperatorComponent,
)
from instill.resources.errors import ComponentTypeExection


class Component:
    def __init__(
        self,
        name: str,
        component: Union[
            ConnectorComponent,
            OperatorComponent,
            IteratorComponent,
        ],
    ):

        if isinstance(component, ConnectorComponent):
            c = Comp(
                id=name,
                connector_component=component,
            )
        elif isinstance(component, OperatorComponent):
            c = Comp(
                id=name,
                operator_component=component,
            )
        elif isinstance(component, IteratorComponent):
            c = Comp(
                id=name,
                iterator_component=component,
            )
        else:
            raise ComponentTypeExection

        self.c = c

    def get_component(self) -> Comp:
        return self.c

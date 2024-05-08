# pylint: disable=no-member,wrong-import-position,no-name-in-module
from instill.resources import Component
from instill.resources.schema import helper, numbers_task_commit_input


class NumbersConnector(Component):
    """Numbers Connector"""

    def __init__(
        self,
        name: str,
        inp: numbers_task_commit_input.Input,
    ) -> None:
        definition_name = "connector-definitions/numbers"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)

# pylint: disable=no-member,wrong-import-position
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_pb
from instill.resources.schema import (
    end_task_end_input,
    end_task_end_metadata,
    start_task_start_metadata,
)


def create_start_operator(
    metadata: start_task_start_metadata.Model,
) -> pipeline_pb.Component:
    start_operator_component = pipeline_pb.Component()
    start_operator_component.id = "start"
    start_operator_component.resource_name = ""
    start_operator_component.definition_name = "operator-definitions/start"
    start_operator_component.configuration.update(metadata)  # type: ignore

    return start_operator_component


def create_end_operator(
    inp: end_task_end_input.Input,
    metadata: end_task_end_metadata.Model,
) -> pipeline_pb.Component:
    end_operator_component = pipeline_pb.Component()
    end_operator_component.id = "end"
    end_operator_component.resource_name = ""
    end_operator_component.definition_name = "operator-definitions/end"
    end_operator_component.configuration.update(inp)
    end_operator_component.configuration.update(metadata)  # type: ignore

    return end_operator_component

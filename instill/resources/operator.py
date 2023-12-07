# pylint: disable=no-member,wrong-import-position
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_pb


def create_start_operator(config: dict) -> pipeline_pb.Component:
    start_operator_component = pipeline_pb.Component()
    start_operator_component.id = "start"
    start_operator_component.definition_name = "operator-definitions/start"
    start_operator_component.configuration.update(config)

    return start_operator_component


def create_end_operator(config: dict) -> pipeline_pb.Component:
    end_operator_component = pipeline_pb.Component()
    end_operator_component.id = "end"
    end_operator_component.definition_name = "operator-definitions/end"
    end_operator_component.configuration.update(config)

    return end_operator_component

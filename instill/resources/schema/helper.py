# pylint: disable=no-member,wrong-import-position,no-name-in-module
import re
from dataclasses import fields, is_dataclass

from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import (
    ConnectorComponent,
    IteratorComponent,
    OperatorComponent,
)


def populate_default_value(dc):
    for field in fields(dc):
        if field.default is None and getattr(dc, field.name) is None:
            list_pattern = re.compile(r"^Optional\[List")
            other_optional_pattern = re.compile(r"^Optional\[")
            if field.type == "Optional[bool]":
                setattr(dc, field.name, False)
            elif field.type == "Optional[str]":
                setattr(dc, field.name, "")
            elif field.type == "Optional[int]":
                setattr(dc, field.name, 0)
            elif field.type == "Optional[float]":
                setattr(dc, field.name, 0.0)
            elif list_pattern.match(field.type):
                setattr(dc, field.name, [])
            elif other_optional_pattern.match(field.type):
                setattr(dc, field.name, {})

    return dc


def pop_default_and_to_dict(dc) -> dict:
    if isinstance(dc, dict):
        return dc

    output_dict = {}
    for field in fields(dc):
        field_val = getattr(dc, field.name)
        if field_val is not None:
            if is_dataclass(field_val):
                field_val = pop_default_and_to_dict(field_val)
            output_dict[field.name] = field_val
    return output_dict


def construct_component_config(
    component_type: str,
    definition_name: str,
    inp,
):
    task_name = str(inp.__class__).split(".")[3]
    prefix = task_name.split("_")[0] + "_"
    suffix = "_" + task_name.split("_")[-1]
    inp = pop_default_and_to_dict(inp)
    task = remove_prefix_and_suffix(
        task_name,
        prefix,
        suffix,
    ).upper()

    if component_type == "connector":
        component = ConnectorComponent(
            definition_name=definition_name,
            task=task,
            input=inp,
        )
    elif component_type == "operator":
        component = OperatorComponent(
            definition_name=definition_name,
            task=task,
            input=inp,
        )
    elif component_type == "iterator":
        component = IteratorComponent()

    return component


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def remove_suffix(text: str, suffix: str) -> str:
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text


def remove_prefix_and_suffix(text: str, prefix: str, suffix: str) -> str:
    text = remove_prefix(text, prefix)
    text = remove_suffix(text, suffix)

    return text

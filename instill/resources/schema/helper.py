import re


def populate_default_value(dataclass):
    for field in dataclass.__dataclass_fields__.values():
        if field.default is None and getattr(dataclass, field.name) is None:
            list_pattern = re.compile(r"^Optional\[List")
            other_optional_pattern = re.compile(r"^Optional\[")
            if field.type == "Optional[bool]":
                setattr(dataclass, field.name, False)
            elif field.type == "Optional[str]":
                setattr(dataclass, field.name, "")
            elif field.type == "Optional[int]":
                setattr(dataclass, field.name, 0)
            elif field.type == "Optional[float]":
                setattr(dataclass, field.name, 0.0)
            elif list_pattern.match(field.type):
                setattr(dataclass, field.name, [])
            elif other_optional_pattern.match(field.type):
                setattr(dataclass, field.name, {})

    return dataclass


def construct_connector_config(inp):
    task_name = str(inp.__class__).split(".")[3]
    prefix = task_name.split("_")[0] + "_"
    suffix = "_" + task_name.split("_")[-1]
    config = {
        "input": vars(inp),
        "task": remove_prefix_and_suffix(
            task_name,
            prefix,
            suffix,
        ).upper(),
    }
    return config


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

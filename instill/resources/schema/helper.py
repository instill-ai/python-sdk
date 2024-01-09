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

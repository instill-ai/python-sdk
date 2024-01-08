def populate_default_value(dataclass):
    for field in dataclass.__dataclass_fields__.values():
        if field.default is None and isinstance(field.type, bool):
            setattr(dataclass, field.name, False)
        if field.default is None and isinstance(field.type, str):
            setattr(dataclass, field.name, "")
        if field.default is None and isinstance(field.type, int):
            setattr(dataclass, field.name, 0)
        if field.default is None and isinstance(field.type, float):
            setattr(dataclass, field.name, 0.0)
        if field.default is None and isinstance(field.type, dict):
            setattr(dataclass, field.name, {})
        if field.default is None and isinstance(field.type, list):
            setattr(dataclass, field.name, [])

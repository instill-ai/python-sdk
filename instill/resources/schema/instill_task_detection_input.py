# generated by datamodel-codegen:
#   filename:  instill_task_detection_input.json
#   timestamp: 2024-01-04T21:51:49+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Model:
    pass


@dataclass
class Common:
    image_base64: str
    model_id: str
    model_namespace: str


@dataclass
class ExtraParam:
    param_name: str
    param_value: str


ExtraParams = List[ExtraParam]

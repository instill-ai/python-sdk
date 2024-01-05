# generated by datamodel-codegen:
#   filename:  instill_task_keypoint_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Model:
    pass


@dataclass
class Input:
    """
    Input
    """

    image_base64: str
    model_id: str
    model_namespace: str


@dataclass
class Param:
    param_name: str
    param_value: str


ExtraParams = List[Param]

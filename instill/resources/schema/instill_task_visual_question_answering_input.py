# generated by datamodel-codegen:
#   filename:  instill_task_visual_question_answering_input.json
#   timestamp: 2024-01-04T21:51:56+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


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


@dataclass
class Input:
    image_base64: str
    model_id: str
    model_namespace: str
    prompt: str
    extra_params: Optional[ExtraParams] = None
    max_new_tokens: Optional[int] = 50
    seed: Optional[int] = None
    temperature: Optional[float] = 0.7
    top_k: Optional[int] = 10

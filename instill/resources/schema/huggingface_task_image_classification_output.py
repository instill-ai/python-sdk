# generated by datamodel-codegen:
#   filename:  huggingface_task_image_classification_output.json
#   timestamp: 2024-01-04T21:51:39+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Class:
    label: str
    score: float


@dataclass
class Output:
    classes: List[Class]


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str

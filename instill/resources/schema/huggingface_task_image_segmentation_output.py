# generated by datamodel-codegen:
#   filename:  huggingface_task_image_segmentation_output.json
#   timestamp: 2024-01-04T21:51:39+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Segment:
    label: str
    mask: str
    score: float


@dataclass
class Output:
    segments: List[Segment]


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str

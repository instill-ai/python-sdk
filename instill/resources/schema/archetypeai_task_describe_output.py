# generated by datamodel-codegen:
#   filename:  archetypeai_task_describe_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class FrameDescription:
    frame_id: int
    timestamp: float
    description: str


@dataclass
class Output:
    descriptions: List[FrameDescription]

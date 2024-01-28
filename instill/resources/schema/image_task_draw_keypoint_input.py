# generated by datamodel-codegen:
#   filename:  image_task_draw_keypoint_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BoundingBox:
    height: float
    left: float
    top: float
    width: float


@dataclass
class Keypoints:
    v: float
    x: float
    y: float


@dataclass
class Object:
    bounding_box: BoundingBox
    keypoints: List[Keypoints]
    score: float


@dataclass
class Input:
    image: str
    objects: List[Object]
    showScore: Optional[bool] = None

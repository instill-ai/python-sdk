# generated by datamodel-codegen:
#   filename:  instill_task_semantic_segmentation_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class Output:
    """
    Output
    """


@dataclass
class Object:
    category: str
    rle: str


@dataclass
class SemanticSegmentation:
    stuffs: List[Object]


InstillTypes = Any


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
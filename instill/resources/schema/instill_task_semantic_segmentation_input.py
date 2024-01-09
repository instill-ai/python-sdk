# generated by datamodel-codegen:
#   filename:  instill_task_semantic_segmentation_input.json

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


@dataclass
class Model:
    pass


@dataclass
class ImageUrl:
    url: str


class Type(Enum):
    text = 'text'
    image_url = 'image_url'


@dataclass
class MultiModalContentItem:
    type: Type
    image_url: Optional[ImageUrl] = None
    text: Optional[str] = None


InstillTypes = Any


@dataclass
class Input:
    image_base64: str
    model_id: str
    model_namespace: str


@dataclass
class ExtraParameters:
    pass


@dataclass
class ChatMessage:
    content: List[MultiModalContentItem]
    role: str

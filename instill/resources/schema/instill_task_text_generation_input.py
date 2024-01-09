# generated by datamodel-codegen:
#   filename:  instill_task_text_generation_input.json

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


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
class Input1:
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


@dataclass
class Input:
    model_id: str
    model_namespace: str
    prompt: str
    chat_history: Optional[List[ChatMessage]] = None
    extra_params: Optional[ExtraParameters] = None
    max_new_tokens: Optional[int] = 50
    prompt_images: Optional[List[str]] = None
    seed: Optional[int] = None
    system_message: Optional[str] = 'You are a helpful assistant.'
    temperature: Optional[float] = 0.7
    top_k: Optional[int] = 10

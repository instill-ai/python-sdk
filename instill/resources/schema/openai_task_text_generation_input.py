# generated by datamodel-codegen:
#   filename:  openai_task_text_generation_input.json

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


class Model(Enum):
    gpt_4_1106_preview = 'gpt-4-1106-preview'
    gpt_4_vision_preview = 'gpt-4-vision-preview'
    gpt_4 = 'gpt-4'
    gpt_4_0314 = 'gpt-4-0314'
    gpt_4_0613 = 'gpt-4-0613'
    gpt_4_32k = 'gpt-4-32k'
    gpt_4_32k_0314 = 'gpt-4-32k-0314'
    gpt_4_32k_0613 = 'gpt-4-32k-0613'
    gpt_3_5_turbo = 'gpt-3.5-turbo'
    gpt_3_5_turbo_16k = 'gpt-3.5-turbo-16k'
    gpt_3_5_turbo_0301 = 'gpt-3.5-turbo-0301'
    gpt_3_5_turbo_0613 = 'gpt-3.5-turbo-0613'
    gpt_3_5_turbo_16k_0613 = 'gpt-3.5-turbo-16k-0613'


class Type(Enum):
    text = 'text'
    json_object = 'json_object'


@dataclass
class ImageUrl:
    url: str


class Type1(Enum):
    text = 'text'
    image_url = 'image_url'


@dataclass
class MultiModalContentItem:
    type: Type1
    image_url: Optional[ImageUrl] = None
    text: Optional[str] = None


InstillTypes = Any


@dataclass
class ResponseFormat:
    type: Type


@dataclass
class ChatMessage:
    content: List[MultiModalContentItem]
    role: str


@dataclass
class Input:
    model: Model
    prompt: str
    chat_history: Optional[List[ChatMessage]] = None
    frequency_penalty: Optional[float] = None
    images: Optional[List[str]] = None
    max_tokens: Optional[int] = None
    n: Optional[int] = None
    presence_penalty: Optional[float] = None
    response_format: Optional[ResponseFormat] = None
    system_message: Optional[str] = 'You are a helpful assistant.'
    temperature: Optional[float] = None
    top_p: Optional[float] = None

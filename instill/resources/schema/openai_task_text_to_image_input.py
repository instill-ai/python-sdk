# generated by datamodel-codegen:
#   filename:  openai_task_text_to_image_input.json
#   timestamp: 2024-01-04T21:52:03+00:00

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Model(Enum):
    dall_e_2 = "dall-e-2"
    dall_e_3 = "dall-e-3"


N = Optional[int]


Prompt = str


class Quality(Enum):
    standard = "standard"
    hd = "hd"


class Size(Enum):
    field_256x256 = "256x256"
    field_512x512 = "512x512"
    field_1024x1024 = "1024x1024"
    field_1792x1024 = "1792x1024"
    field_1024x1792 = "1024x1792"


class Style(Enum):
    vivid = "vivid"
    natural = "natural"


@dataclass
class ChatMessage:
    content: str
    role: str


@dataclass
class Input:
    model: Model
    prompt: Prompt
    n: Optional[N] = None
    quality: Optional[Quality] = Quality.standard
    size: Optional[Size] = Size.field_1024x1024
    style: Optional[Style] = Style.vivid

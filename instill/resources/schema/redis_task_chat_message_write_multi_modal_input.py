# generated by datamodel-codegen:
#   filename:  redis_task_chat_message_write_multi_modal_input.json

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


@dataclass
class ImageUrl:
    url: str


class Type(Enum):
    text = 'text'
    image_url = 'image_url'


@dataclass
class ContentItem:
    type: Type
    image_url: Optional[ImageUrl] = None
    text: Optional[str] = None


@dataclass
class Input:
    content: List[ContentItem]
    role: str
    session_id: str
    metadata: Optional[Dict[str, Any]] = None

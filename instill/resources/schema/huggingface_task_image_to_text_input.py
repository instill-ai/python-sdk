# generated by datamodel-codegen:
#   filename:  huggingface_task_image_to_text_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Input:
    image: str
    model: Optional[str] = None

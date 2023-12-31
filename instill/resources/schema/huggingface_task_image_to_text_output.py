# generated by datamodel-codegen:
#   filename:  huggingface_task_image_to_text_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Output:
    text: str


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str

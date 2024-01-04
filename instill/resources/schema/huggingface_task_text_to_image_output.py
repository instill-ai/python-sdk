# generated by datamodel-codegen:
#   filename:  huggingface_task_text_to_image_output.json
#   timestamp: 2024-01-04T21:51:45+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Output:
    image: str


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str

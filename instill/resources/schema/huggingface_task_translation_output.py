# generated by datamodel-codegen:
#   filename:  huggingface_task_translation_output.json
#   timestamp: 2024-01-04T21:51:46+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Output:
    translation_text: str


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str

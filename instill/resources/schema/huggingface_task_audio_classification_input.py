# generated by datamodel-codegen:
#   filename:  huggingface_task_audio_classification_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Input:
    audio: str
    model: Optional[str] = None

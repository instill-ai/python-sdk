# generated by datamodel-codegen:
#   filename:  huggingface_task_speech_recognition_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Input:
    audio: str
    model: Optional[str] = None

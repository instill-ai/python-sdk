# generated by datamodel-codegen:
#   filename:  instill_task_classification_input.json

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Input:
    image_base64: str
    model_name: str

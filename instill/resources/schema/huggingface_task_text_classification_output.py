# generated by datamodel-codegen:
#   filename:  huggingface_task_text_classification_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Result:
    label: str
    score: float


@dataclass
class Output:
    results: List[Result]

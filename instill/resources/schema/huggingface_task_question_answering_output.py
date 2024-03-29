# generated by datamodel-codegen:
#   filename:  huggingface_task_question_answering_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Output:
    answer: str
    score: Optional[float] = None
    start: Optional[int] = None
    stop: Optional[int] = None

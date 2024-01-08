# generated by datamodel-codegen:
#   filename:  huggingface_task_sentence_similarity_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Output:
    scores: List[float]


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str

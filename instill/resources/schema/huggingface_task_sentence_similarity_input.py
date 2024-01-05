# generated by datamodel-codegen:
#   filename:  huggingface_task_sentence_similarity_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Inputs:
    sentences: List[str]
    source_sentence: str


Model = str


@dataclass
class Options:
    use_cache: Optional[bool]
    wait_for_model: Optional[bool]


StringInput = str


@dataclass
class Input:
    inputs: Inputs
    model: Optional[Model]
    options: Optional[Options]

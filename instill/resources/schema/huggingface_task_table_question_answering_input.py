# generated by datamodel-codegen:
#   filename:  huggingface_task_table_question_answering_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Inputs:
    query: str
    table: Dict[str, Any]


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


@dataclass
class Input:
    inputs: Inputs
    model: Optional[str] = None
    options: Optional[Options] = None

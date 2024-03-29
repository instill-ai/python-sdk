# generated by datamodel-codegen:
#   filename:  huggingface_task_zero_shot_classification_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


@dataclass
class Parameters:
    candidate_labels: List[str]
    multi_label: Optional[bool] = None


@dataclass
class Input:
    inputs: str
    parameters: Parameters
    model: Optional[str] = None
    options: Optional[Options] = None

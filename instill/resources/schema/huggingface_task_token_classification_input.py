# generated by datamodel-codegen:
#   filename:  huggingface_task_token_classification_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Parameters:
    aggregation_strategy: Optional[str] = None


Model = str


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


StringInput = str


@dataclass
class Input:
    inputs: StringInput
    model: Optional[Model] = None
    options: Optional[Options] = None
    parameters: Optional[Parameters] = None

# generated by datamodel-codegen:
#   filename:  archetypeai_task_describe_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Input:
    query: str
    file_ids: List[str]
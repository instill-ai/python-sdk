# generated by datamodel-codegen:
#   filename:  openai_task_text_embeddings_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Output:
    embedding: List[float]

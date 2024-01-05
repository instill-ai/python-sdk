# generated by datamodel-codegen:
#   filename:  text_task_split_by_token_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Output:
    """
    Output
    """

    chunk_num: int
    text_chunks: List[str]
    token_count: int

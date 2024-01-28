# generated by datamodel-codegen:
#   filename:  googlesearch_task_search_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Input:
    query: str
    include_link_html: Optional[bool] = False
    include_link_text: Optional[bool] = False
    top_k: Optional[int] = 10

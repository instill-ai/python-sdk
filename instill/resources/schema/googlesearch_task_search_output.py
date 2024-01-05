# generated by datamodel-codegen:
#   filename:  googlesearch_task_search_output.json

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Result:
    link: str
    link_html: Optional[str]
    link_text: Optional[str]
    snippet: str
    title: str


@dataclass
class Output:
    results: List[Result]
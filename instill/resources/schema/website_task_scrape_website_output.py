# generated by datamodel-codegen:
#   filename:  website_task_scrape_website_output.json
#   timestamp: 2024-01-04T21:52:17+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PageInfo:
    link: str
    link_html: Optional[str] = None
    link_text: Optional[str] = None
    title: Optional[str] = None


@dataclass
class Output:
    pages: List[PageInfo]

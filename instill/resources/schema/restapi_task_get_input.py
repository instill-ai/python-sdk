# generated by datamodel-codegen:
#   filename:  restapi_task_get_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class InputWithoutBody:
    endpoint_url: str
    output_body_schema: Optional[str] = None

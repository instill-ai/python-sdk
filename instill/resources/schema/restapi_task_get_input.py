# generated by datamodel-codegen:
#   filename:  restapi_task_get_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Input:
    body: Optional[Dict[str, Any]]
    endpoint_path: str


@dataclass
class Input1:
    endpoint_path: str


@dataclass
class Output:
    """
    The HTTP response from the API
    """

    body: Dict[str, Any]
    header: Dict[str, Any]
    status_code: int


Model = Input1

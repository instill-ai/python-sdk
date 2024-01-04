# generated by datamodel-codegen:
#   filename:  redis_task_chat_history_retrieve_input.json
#   timestamp: 2024-01-04T21:52:08+00:00

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Input:
    session_id: str
    include_system_message: Optional[bool] = True
    latest_k: Optional[int] = 5


@dataclass
class Message:
    content: str
    role: str
    metadata: Optional[Dict[str, Any]] = None

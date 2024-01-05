# generated by datamodel-codegen:
#   filename:  image_task_draw_classification_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

Category = str


InstillTypes = Any


Score = float


@dataclass
class Input:
    """
    Input
    """

    category: Category
    image: str
    score: Score
    showScore: Optional[bool]
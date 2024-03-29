# generated by datamodel-codegen:
#   filename:  huggingface_task_text_to_image_input.json

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Options:
    use_cache: Optional[bool] = None
    wait_for_model: Optional[bool] = None


@dataclass
class Parameters:
    guidance_scale: Optional[float] = None
    height: Optional[int] = None
    negative_prompt: Optional[str] = None
    num_inference_steps: Optional[int] = None
    width: Optional[int] = None


@dataclass
class Input:
    inputs: str
    model: Optional[str] = None
    options: Optional[Options] = None
    parameters: Optional[Parameters] = None

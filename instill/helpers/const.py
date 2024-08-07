import os
from typing import Dict, List, Sequence, Union

from PIL import Image

PROMPT_ROLES = ["user", "assistant", "system"]


class VisionInput:
    image: Image.Image


class ChatInput:
    messages: List[Dict[str, str]]
    max_tokens: int = 50
    n: int = 1
    seed: int = 0
    temperature: float = 0.7
    top_p: int = 1
    stream: bool = False


class ChatMultiModelInput:
    messages: List[Union[Dict[str, str], Dict[str, Sequence]]]
    prompt_images: Union[List[Image.Image], None] = None
    max_tokens: int = 50
    n: int = 1
    seed: int = 0
    temperature: float = 0.7
    top_p: int = 1
    stream: bool = False


class TextToImageInput:
    prompt = ""
    steps: int = 5
    cfg_scale: float = 7.5
    seed: int = 0
    samples: int = 1
    extra_params: Dict[str, str] = {}


class ImageToImageInput:
    prompt = ""
    steps: int = 5
    cfg_scale: float = 7.5
    seed: int = 0
    samples: int = 1
    low_threshold = 100
    high_threshold = 200
    extra_params: Dict[str, str] = {}


DEFAULT_RAY_ACTOR_OPTIONS = {
    "num_cpus": 0,
}
DEFAULT_AUTOSCALING_CONFIG = {
    "target_ongoing_requests": 2,
    "initial_replicas": 1,
    "min_replicas": 0,
    "max_replicas": 1,
    "upscale_delay_s": 600,
    "downscale_delay_s": 1800,
    "smoothing_factor": 1.0,
    "upscaling_factor": 0.8,
    "downscaling_factor": 0.8,
    "metrics_interval_s": 2,
    "look_back_period_s": 4,
}
DEFAULT_RUNTIME_ENV = {
    "env_vars": {
        "PYTHONPATH": os.getcwd(),
    },
}
DEFAULT_MAX_ONGOING_REQUESTS = 5
DEFAULT_MAX_QUEUED_REQUESTS = 10

RAM_MINIMUM_RESERVE = 1  # GB
RAM_UPSCALE_FACTOR = 1.25
VRAM_MINIMUM_RESERVE = 2  # GB
VRAM_UPSCALE_FACTOR = 1.25

DEFAULT_DEPENDENCIES = ["protobuf==4.25.3", "grpcio-tools==1.62.0"]

ENV_MEMORY = "RAY_MEMORY"
ENV_TOTAL_VRAM = "RAY_TOTAL_VRAM"
ENV_RAY_ACCELERATOR_TYPE = "RAY_ACCELERATOR_TYPE"
ENV_RAY_CUSTOM_RESOURCE = "RAY_CUSTOM_RESOURCE"
ENV_NUM_OF_GPUS = "RAY_NUM_OF_GPUS"
ENV_NUM_OF_CPUS = "RAY_NUM_OF_CPUS"
ENV_NUM_OF_MIN_REPLICAS = "RAY_NUM_OF_MIN_REPLICAS"
ENV_NUM_OF_MAX_REPLICAS = "RAY_NUM_OF_MAX_REPLICAS"
ENV_IS_TEST_MODEL = "RAY_IS_TEST_MODEL"

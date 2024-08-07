import os
from enum import Enum
from typing import Any, Dict, List, Union

import numpy as np


class DataType(Enum):
    TYPE_BOOL = 1
    TYPE_UINT8 = 2
    TYPE_UINT16 = 3
    TYPE_UINT32 = 4
    TYPE_UINT64 = 5
    TYPE_INT8 = 6
    TYPE_INT16 = 7
    TYPE_INT32 = 8
    TYPE_INT64 = 9
    TYPE_FP16 = 10
    TYPE_FP32 = 11
    TYPE_FP64 = 12
    TYPE_STRING = 13


class TextGenerationInput:
    prompt = ""
    prompt_images: Union[List[np.ndarray], None] = None
    chat_history: Union[List[str], None] = None
    system_message: Union[str, None] = None
    max_new_tokens = 100
    temperature = 0.8
    top_k = 1
    random_seed = 0
    stop_words: Any = ""  # Optional
    extra_params: Dict[str, str] = {}


class TextToImageInput:
    prompt_image: Union[np.ndarray, None] = None
    prompt = ""
    negative_prompt = ""
    steps = 5
    guidance_scale = 7.5
    seed = 0
    samples = 1
    extra_params: Dict[str, str] = {}


class ImageToImageInput:
    prompt_image: Union[np.ndarray, None] = None
    prompt = ""
    steps = 5
    guidance_scale = 7.5
    seed = 0
    samples = 1
    extra_params: Dict[str, str] = {}


class TextGenerationChatInput:
    prompt = ""
    prompt_images: Union[List[np.ndarray], None] = None
    chat_history: Union[List[str], None] = None
    system_message: Union[str, None] = None
    max_new_tokens = 100
    temperature = 0.8
    top_k = 1
    random_seed = 0
    stop_words: Any = ""  # Optional
    extra_params: Dict[str, str] = {}


class VisualQuestionAnsweringInput:
    prompt = ""
    prompt_images: Union[List[np.ndarray], None] = None
    chat_history: Union[List[str], None] = None
    system_message: Union[str, None] = None
    max_new_tokens = 100
    temperature = 0.8
    top_k = 1
    random_seed = 0
    stop_words: Any = ""  # Optional
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

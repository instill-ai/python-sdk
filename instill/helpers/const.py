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


DEFAULT_RAY_ACTOR_OPRTIONS = {
    "num_cpus": 2,
}
DEFAULT_AUTOSCALING_CONFIG = {
    "target_num_ongoing_requests_per_replica": 1,
    "initial_replicas": 1,
    "min_replicas": 0,
    "max_replicas": 8,
    "upscale_delay_s": 10,
    "downscale_delay_s": 600,
    "smoothing_factor": 0.8,
    "upscale_smoothing_factor": 0.8,
    "downscale_smoothing_factor": 0.3,
    "metrics_interval_s": 2,
    "look_back_period_s": 4,
}
DEFAULT_RUNTIME_ENV = {
    "env_vars": {
        "PYTHONPATH": os.getcwd(),
    },
}
DEFAULT_MAX_CONCURRENT_QUERIES = 10

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
    "max_replicas": 10,
    "upscale_delay_s": 4,
    "downscale_delay_s": 600,
    "smoothing_factor": 1.0,
    "upscale_smoothing_factor": 0.8,
    "downscale_smoothing_factor": 0.8,
    "metrics_interval_s": 2,
    "look_back_period_s": 4,
}
DEFAULT_RUNTIME_ENV = {
    "env_vars": {
        "PYTHONPATH": os.getcwd(),
    },
}
DEFAULT_MAX_CONCURRENT_QUERIES = 5

RAM_MINIMUM_RESERVE = 1  # GB
RAM_UPSCALE_FACTOR = 1.25
VRAM_MINIMUM_RESERVE = 2  # GB
VRAM_UPSCALE_FACTOR = 1.25

MODEL_VRAM_OVERRIDE_LIST = {
    "stable-diffusion-xl": 0.375,
    "controlnet-canny": 0.375,
    "llava-1-6-7b": 0.2,
    "llava-1-6-13b": 0.7,
    "llama2-7b-chat": 0.3,
    "llama2-7b": 0.4,
    "zephyr-7b": 0.4,
}

DEFAULT_DEPENDENCIES = ["protobuf==4.25.3", "grpcio-tools==1.62.0"]

# ray accelerators
NVIDIA_TESLA_V100 = "V100"
NVIDIA_TESLA_P100 = "P100"
NVIDIA_TESLA_T4 = "T4"
NVIDIA_TESLA_P4 = "P4"
NVIDIA_TESLA_K80 = "K80"
NVIDIA_TESLA_A10G = "A10G"
NVIDIA_L4 = "L4"
NVIDIA_A100 = "A100"
INTEL_MAX_1550 = "Intel-GPU-Max-1550"
INTEL_MAX_1100 = "Intel-GPU-Max-1100"
INTEL_GAUDI = "Intel-GAUDI"
AMD_INSTINCT_MI100 = "AMD-Instinct-MI100"
AMD_INSTINCT_MI250X = "AMD-Instinct-MI250X"
AMD_INSTINCT_MI250 = "AMD-Instinct-MI250X-MI250"
AMD_INSTINCT_MI210 = "AMD-Instinct-MI210"
AMD_INSTINCT_MI300X = "AMD-Instinct-MI300X-OAM"
AMD_RADEON_R9_200_HD_7900 = "AMD-Radeon-R9-200-HD-7900"
AMD_RADEON_HD_7900 = "AMD-Radeon-HD-7900"
AWS_NEURON_CORE = "aws-neuron-core"
GOOGLE_TPU_V2 = "TPU-V2"
GOOGLE_TPU_V3 = "TPU-V3"
GOOGLE_TPU_V4 = "TPU-V4"

# Use these instead of NVIDIA_A100 if you need a specific accelerator size. Note that
# these labels are not auto-added to nodes, you'll have to add them manually in
# addition to the default A100 label if needed.
NVIDIA_A100_40G = "A100-40G"
NVIDIA_A100_80G = "A100-80G"

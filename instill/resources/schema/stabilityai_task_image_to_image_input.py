# generated by datamodel-codegen:
#   filename:  stabilityai_task_image_to_image_input.json

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ClipGuidancePreset(Enum):
    FAST_BLUE = 'FAST_BLUE'
    FAST_GREEN = 'FAST_GREEN'
    NONE = 'NONE'
    SIMPLE = 'SIMPLE'
    SLOW = 'SLOW'
    SLOWER = 'SLOWER'
    SLOWEST = 'SLOWEST'


class Engine(Enum):
    stable_diffusion_xl_1024_v1_0 = 'stable-diffusion-xl-1024-v1-0'
    stable_diffusion_xl_1024_v0_9 = 'stable-diffusion-xl-1024-v0-9'
    stable_diffusion_v1_6 = 'stable-diffusion-v1-6'
    esrgan_v1_x2plus = 'esrgan-v1-x2plus'
    stable_diffusion_512_v2_1 = 'stable-diffusion-512-v2-1'
    stable_diffusion_xl_beta_v2_2_2 = 'stable-diffusion-xl-beta-v2-2-2'


class InitImageMode(Enum):
    IMAGE_STRENGTH = 'IMAGE_STRENGTH'
    STEP_SCHEDULE = 'STEP_SCHEDULE'


class Sampler(Enum):
    DDIM = 'DDIM'
    DDPM = 'DDPM'
    K_DPMPP_2M = 'K_DPMPP_2M'
    K_DPMPP_2S_ANCESTRAL = 'K_DPMPP_2S_ANCESTRAL'
    K_DPM_2 = 'K_DPM_2'
    K_DPM_2_ANCESTRAL = 'K_DPM_2_ANCESTRAL'
    K_EULER = 'K_EULER'
    K_EULER_ANCESTRAL = 'K_EULER_ANCESTRAL'
    K_HEUN = 'K_HEUN'
    K_LMS = 'K_LMS'


class StylePreset(Enum):
    enhance = 'enhance'
    anime = 'anime'
    photographic = 'photographic'
    digital_art = 'digital-art'
    comic_book = 'comic-book'
    fantasy_art = 'fantasy-art'
    line_art = 'line-art'
    analog_film = 'analog-film'
    neon_punk = 'neon-punk'
    isometric = 'isometric'
    low_poly = 'low-poly'
    origami = 'origami'
    modeling_compound = 'modeling-compound'
    cinematic = 'cinematic'
    field_3d_model = '3d-model'
    pixel_art = 'pixel-art'
    tile_texture = 'tile-texture'


@dataclass
class Input:
    engine: Engine
    prompts: List[str]
    cfg_scale: Optional[float] = 7
    clip_guidance_preset: Optional[ClipGuidancePreset] = ClipGuidancePreset.NONE
    image_strength: Optional[float] = 0.35
    init_image: Optional[bytes] = None
    init_image_mode: Optional[InitImageMode] = InitImageMode.IMAGE_STRENGTH
    sampler: Optional[Sampler] = None
    samples: Optional[int] = 1
    seed: Optional[int] = 0
    step_schedule_end: Optional[float] = None
    step_schedule_start: Optional[float] = 0.65
    steps: Optional[int] = 30
    style_preset: Optional[StylePreset] = None
    weights: Optional[List[float]] = None

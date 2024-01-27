import math
import os
from typing import Callable, Optional

import ray
from ray import serve
from ray.serve import Deployment
from ray.serve import deployment as ray_deployment

from instill.helpers.const import (
    DEFAULT_AUTOSCALING_CONFIG,
    DEFAULT_MAX_CONCURRENT_QUERIES,
    DEFAULT_RAY_ACTOR_OPRTIONS,
    DEFAULT_RUNTIME_ENV,
    VRAM_MINIMUM_RESERVE,
    VRAM_UPSCALE_FACTOR,
)
from instill.helpers.errors import ModelPathException
from instill.helpers.utils import get_dir_size


class InstillDeployable:
    def __init__(
        self,
        deployable: Deployment,
        model_weight_or_folder_name: str,
        use_gpu: bool,
    ) -> None:
        self._deployment: Deployment = deployable
        self.use_gpu = use_gpu
        # params
        self.model_weight_or_folder_name: str = model_weight_or_folder_name
        if use_gpu:
            self._update_num_cpus(2)
            self._update_num_gpus(0.25)
        else:
            self._update_num_cpus(4)

    def _update_num_cpus(self, num_cpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_cpus": num_cpus})

    def _update_memory(self, memory: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"memory": memory})

    def _update_num_gpus(self, num_gpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_gpus": num_gpus})

    def _determine_vram_usage(self, model_path: str, vram: str):
        if vram == "":
            return 0.25
        if os.path.isfile(model_path):
            min_vram_usage = max(
                VRAM_MINIMUM_RESERVE,
                VRAM_UPSCALE_FACTOR
                * os.path.getsize(model_path)
                / (1024 * 1024 * 1024),
            )
            ratio = min_vram_usage / float(vram)
            return ratio if ratio <= 1 else math.ceil(ratio)
        if os.path.isdir(model_path):
            min_vram_usage = max(
                VRAM_MINIMUM_RESERVE,
                VRAM_UPSCALE_FACTOR * get_dir_size(model_path) / (1024 * 1024 * 1024),
            )
            ratio = min_vram_usage / float(vram)
            return ratio if ratio <= 1 else math.ceil(ratio)
        raise ModelPathException

    def _determine_ram_usage(self, model_path: str):
        if os.path.isfile(model_path):
            return 1.1 * os.path.getsize(model_path)
        if os.path.isdir(model_path):
            return 1.1 * get_dir_size(model_path)
        raise ModelPathException

    def update_min_replicas(self, num_replicas: int):
        new_autoscaling_config = DEFAULT_AUTOSCALING_CONFIG
        new_autoscaling_config["min_replicas"] = num_replicas
        self._deployment = self._deployment.options(
            autoscaling_config=new_autoscaling_config
        )

    def update_max_replicas(self, num_replicas: int):
        new_autoscaling_config = DEFAULT_AUTOSCALING_CONFIG
        new_autoscaling_config["max_replicas"] = num_replicas
        self._deployment = self._deployment.options(
            autoscaling_config=new_autoscaling_config
        )

    def deploy(self, model_folder_path: str, ray_addr: str, vram: str):
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)

        model_path = "/".join([model_folder_path, self.model_weight_or_folder_name])
        model_path_string_parts = model_path.split("/")
        application_name = model_path_string_parts[5]
        model_name = "_".join(model_path_string_parts[3].split("#")[:2])
        route_prefix = f'/{model_name}/{model_path_string_parts[3].split("#")[3]}'

        if self.use_gpu:
            self._update_num_gpus(self._determine_vram_usage(model_path, vram))
        else:
            self._update_memory(self._determine_ram_usage(model_path))

        serve.run(
            self._deployment.options(name=application_name).bind(model_path),
            name=model_name,
            route_prefix=route_prefix,
        )

    def undeploy(self, model_folder_path: str, ray_addr: str):
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)
        model_path = "/".join([model_folder_path, self.model_weight_or_folder_name])
        model_path_string_parts = model_path.split("/")
        model_name = "_".join(model_path_string_parts[3].split("#")[:2])
        serve.delete(model_name)

    def __call__(self):
        raise RuntimeError(
            "Deployments cannot be constructed directly. Use `deploy()` instead."
        )


def instill_deployment(
    _func_or_class: Optional[Callable] = None,
) -> Callable[[Callable], InstillDeployable]:
    return ray_deployment(
        _func_or_class=_func_or_class,
        ray_actor_options=DEFAULT_RAY_ACTOR_OPRTIONS,
        autoscaling_config=DEFAULT_AUTOSCALING_CONFIG,
        max_concurrent_queries=DEFAULT_MAX_CONCURRENT_QUERIES,
    )

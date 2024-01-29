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
    MODEL_VRAM_OVERRIDE_LIST,
    RAM_MINIMUM_RESERVE,
    RAM_UPSCALE_FACTOR,
    VRAM_MINIMUM_RESERVE,
    VRAM_UPSCALE_FACTOR,
)
from instill.helpers.errors import ModelPathException, ModelVramException
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
            self._update_num_cpus(1)
            self._update_num_gpus(0.25)
        else:
            self._update_num_cpus(2)

    def _update_num_cpus(self, num_cpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_cpus": num_cpus})

    def _update_memory(self, memory: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"memory": memory})

    def _update_num_gpus(self, num_gpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_gpus": num_gpus})

    def _determine_vram_usage(self, model_path: str, total_vram: str):
        if total_vram == "":
            return 0.25
        if os.path.isfile(model_path):
            min_vram_usage = max(
                VRAM_MINIMUM_RESERVE,
                VRAM_UPSCALE_FACTOR
                * os.path.getsize(model_path)
                / (1024 * 1024 * 1024),
            )
            ratio = min_vram_usage / float(total_vram)
            if ratio > 1:
                raise ModelVramException
            return ratio
        if os.path.isdir(model_path):
            min_vram_usage = max(
                VRAM_MINIMUM_RESERVE,
                VRAM_UPSCALE_FACTOR * get_dir_size(model_path) / (1024 * 1024 * 1024),
            )
            ratio = min_vram_usage / float(total_vram)
            if ratio > 1:
                raise ModelVramException
            return ratio
        raise ModelPathException

    def _determine_ram_usage(self, model_path: str):
        if os.path.isfile(model_path):
            return max(
                RAM_MINIMUM_RESERVE * (1024 * 1024 * 1024),
                RAM_UPSCALE_FACTOR * os.path.getsize(model_path),
            )
        if os.path.isdir(model_path):
            return max(
                RAM_MINIMUM_RESERVE * (1024 * 1024 * 1024),
                RAM_UPSCALE_FACTOR * get_dir_size(model_path),
            )
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

    def deploy(self, model_folder_path: str, ray_addr: str, total_vram: str):
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)

        model_path = "/".join([model_folder_path, self.model_weight_or_folder_name])
        model_path_string_parts = model_path.split("/")
        application_name = "_".join(model_path_string_parts[3].split("#")[:2])
        model_name = application_name.split("_")[1]

        if self.use_gpu:
            if model_name in MODEL_VRAM_OVERRIDE_LIST:
                self._update_num_gpus(MODEL_VRAM_OVERRIDE_LIST[model_name])
            else:
                self._update_num_gpus(
                    self._determine_vram_usage(model_path, total_vram)
                )
        else:
            self._update_memory(self._determine_ram_usage(model_path))

        if model_name in MODEL_VRAM_OVERRIDE_LIST:
            self.update_min_replicas(1)
            self.update_max_replicas(1)

        serve.run(
            self._deployment.options(name=model_name).bind(model_path),
            name=application_name,
            route_prefix=f"/{application_name}",
        )

    def undeploy(self, model_folder_path: str, ray_addr: str):
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)
        model_path = "/".join([model_folder_path, self.model_weight_or_folder_name])
        model_path_string_parts = model_path.split("/")
        application_name = "_".join(model_path_string_parts[3].split("#")[:2])
        serve.delete(application_name)

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

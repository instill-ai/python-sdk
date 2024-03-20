# pylint: disable=unused-argument
import os
from typing import Callable, Optional
from warnings import warn

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
        model_weight_or_folder_name: str,  # kept for backward compatibility
        use_gpu: bool,
    ) -> None:
        self._deployment: Deployment = deployable
        self.use_gpu = use_gpu
        # params
        if use_gpu:
            self.update_num_cpus(0.25)
            self.update_num_gpus(0.2)
        else:
            self.update_num_cpus(0.25)

    def update_num_cpus(self, num_cpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_cpus": num_cpus})

        return self

    def update_memory(self, memory: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"memory": memory})

        return self

    def update_num_gpus(self, num_gpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_gpus": num_gpus})

        return self

    def update_accelerator_type(self, accelerator_type: str):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update(
                {"accelerator_type": accelerator_type}
            )

        return self

    def update_num_custom_resource(self, resource_name: str, num: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update(
                {"resources": {resource_name: num}}
            )

        return self

    def _determine_vram_usage(self, model_path: str, total_vram: str):
        warn(
            "determine vram usage base on file size will soon be removed",
            PendingDeprecationWarning,
        )
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
        warn(
            "determine ram usage base on file size will soon be removed",
            PendingDeprecationWarning,
        )
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

        return self

    def update_max_replicas(self, num_replicas: int):
        new_autoscaling_config = DEFAULT_AUTOSCALING_CONFIG
        new_autoscaling_config["max_replicas"] = num_replicas
        self._deployment = self._deployment.options(
            autoscaling_config=new_autoscaling_config
        )

        return self

    def get_deployment_handle(self):
        return self._deployment.bind()

    def deploy(self, model_folder_path: str, ray_addr: str, total_vram: str):
        warn(
            "Deploy/Undeploy will soon be remove from the scope of SDK",
            PendingDeprecationWarning,
        )
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)

        # /model-repository/{owner_type}/{owner_uid}/{model_id}
        model_path_string_parts = model_folder_path.split("/")
        application_name = "_".join(model_path_string_parts[3:])
        model_name = application_name.split("_")[1]

        if self.use_gpu:
            if model_name in MODEL_VRAM_OVERRIDE_LIST:
                self.update_num_gpus(MODEL_VRAM_OVERRIDE_LIST[model_name])
            else:
                self.update_num_gpus(
                    self._determine_vram_usage(model_folder_path, total_vram)
                )
        else:
            self.update_memory(self._determine_ram_usage(model_folder_path))

        if model_name in MODEL_VRAM_OVERRIDE_LIST:
            self.update_min_replicas(1)
            self.update_max_replicas(1)

        serve.run(
            # kept model_folder_path for backward compatibility
            self._deployment.options(name=model_name).bind(model_folder_path),
            name=application_name,
            route_prefix=f"/{application_name}",
        )

    def undeploy(self, model_folder_path: str, ray_addr: str):
        warn(
            "Deploy/Undeploy will soon be remove from the scope of SDK",
            PendingDeprecationWarning,
        )
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)
        # /model-repository/{owner_type}/{owner_uid}/{model_id}
        model_path_string_parts = model_folder_path.split("/")
        application_name = "_".join(model_path_string_parts[3:])
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

import os
from typing import Callable, Optional
from warnings import warn

from ray.serve import Deployment
from ray.serve import deployment as ray_deployment

from instill.helpers.const import (
    DEFAULT_AUTOSCALING_CONFIG,
    DEFAULT_MAX_ONGOING_REQUESTS,
    DEFAULT_MAX_QUEUED_REQUESTS,
    DEFAULT_RAY_ACTOR_OPTIONS,
    ENV_IS_TEST_MODEL,
    ENV_MEMORY,
    ENV_NUM_OF_CPUS,
    ENV_NUM_OF_GPUS,
    ENV_NUM_OF_MAX_REPLICAS,
    ENV_NUM_OF_MIN_REPLICAS,
    ENV_RAY_ACCELERATOR_TYPE,
    ENV_RAY_CUSTOM_RESOURCE,
    ENV_TOTAL_VRAM,
    RAM_MINIMUM_RESERVE,
    RAM_UPSCALE_FACTOR,
    VRAM_MINIMUM_RESERVE,
    VRAM_UPSCALE_FACTOR,
)
from instill.helpers.errors import ModelPathException
from instill.helpers.utils import get_dir_size


class InstillDeployable:
    def __init__(self, deployable: Deployment) -> None:
        self._deployment: Deployment = deployable
        self._autoscaling_config = DEFAULT_AUTOSCALING_CONFIG.copy()

        num_of_cpus = os.getenv(ENV_NUM_OF_CPUS)
        if num_of_cpus is not None and num_of_cpus != "":
            self._update_num_cpus(float(num_of_cpus))

        is_test_model = os.getenv(ENV_IS_TEST_MODEL)
        if is_test_model is not None and is_test_model.lower() == "true":
            self._update_num_cpus(float(0.001))
            self._update_downscale_delay(60)

        memory = os.getenv(ENV_MEMORY)
        if memory is not None and memory != "":
            self._update_memory(float(memory))

        num_of_gpus = os.getenv(ENV_NUM_OF_GPUS)
        vram = os.getenv(ENV_TOTAL_VRAM)
        if vram is not None and vram != "":
            self._update_num_gpus(self._determine_vram_usage(os.getcwd(), vram))
        elif num_of_gpus is not None and num_of_gpus != "":
            self._update_num_gpus(float(num_of_gpus))

        num_of_gpus = self._deployment.ray_actor_options.get(  # type: ignore
            "num_gpus", 0.001
        )

        accelerator_type = os.getenv(ENV_RAY_ACCELERATOR_TYPE)
        if accelerator_type is not None and accelerator_type != "":
            self._update_accelerator_type(accelerator_type)

        custom_resource = os.getenv(ENV_RAY_CUSTOM_RESOURCE)
        if custom_resource is not None and custom_resource != "":
            self._update_custom_resource(custom_resource, num_of_gpus)

        num_of_min_replicas = os.getenv(ENV_NUM_OF_MIN_REPLICAS)
        if num_of_min_replicas is not None and num_of_min_replicas != "":
            self._update_min_replicas(int(num_of_min_replicas))
        else:
            self._update_min_replicas(0)

        num_of_max_replicas = os.getenv(ENV_NUM_OF_MAX_REPLICAS)
        if num_of_max_replicas is not None and num_of_max_replicas != "":
            self._update_max_replicas(int(num_of_max_replicas))
        else:
            self._update_max_replicas(1)

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
                warn(
                    "model projected vram usage is more than the GPU can handle, \
                    deployment might result in error state"
                )
                ratio = 1
            return ratio
        if os.path.isdir(model_path):
            min_vram_usage = max(
                VRAM_MINIMUM_RESERVE,
                VRAM_UPSCALE_FACTOR * get_dir_size(model_path) / (1024 * 1024 * 1024),
            )
            ratio = min_vram_usage / float(total_vram)
            if ratio > 1:
                warn(
                    "model projected vram usage is more than the GPU can handle, \
                    deployment might result in error state"
                )
                ratio = 1
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

    def _update_num_cpus(self, num_cpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_cpus": num_cpus})

        return self

    def _update_memory(self, memory: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"memory": memory})

        return self

    def _update_num_gpus(self, num_gpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_gpus": num_gpus})

        return self

    def _update_accelerator_type(self, accelerator_type: str):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update(
                {"accelerator_type": accelerator_type}
            )

        return self

    def _update_custom_resource(self, resource_name: str, ratio=0.001):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update(
                {"resources": {resource_name: ratio}}
            )

        return self

    def _update_min_replicas(self, num_replicas: int):
        self._autoscaling_config["min_replicas"] = num_replicas
        self._deployment = self._deployment.options(
            autoscaling_config=self._autoscaling_config
        )

        return self

    def _update_max_replicas(self, num_replicas: int):
        self._autoscaling_config["max_replicas"] = num_replicas
        self._deployment = self._deployment.options(
            autoscaling_config=self._autoscaling_config
        )

        return self

    def _update_downscale_delay(self, downscale_delay_s: int):
        self._autoscaling_config["downscale_delay_s"] = downscale_delay_s

    def get_deployment_handle(self):
        return self._deployment.bind()


def instill_deployment(
    _func_or_class: Optional[Callable] = None,
) -> Callable[[Callable], InstillDeployable]:
    return ray_deployment(
        _func_or_class=_func_or_class,
        ray_actor_options=DEFAULT_RAY_ACTOR_OPTIONS,
        autoscaling_config=DEFAULT_AUTOSCALING_CONFIG,
        max_ongoing_requests=DEFAULT_MAX_ONGOING_REQUESTS,
        max_queued_requests=DEFAULT_MAX_QUEUED_REQUESTS,
    )

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
)


class InstillDeployable:
    def __init__(
        self,
        deployable: Deployment,
        model_weight_or_folder_name: str,
        use_gpu: bool,
    ) -> None:
        self._deployment: Deployment = deployable
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

    def _update_num_gpus(self, num_gpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_gpus": num_gpus})

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

    def deploy(self, model_folder_path: str, ray_addr: str):
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(address=ray_addr, runtime_env=DEFAULT_RUNTIME_ENV)
        model_path = "/".join([model_folder_path, self.model_weight_or_folder_name])
        model_path_string_parts = model_path.split("/")
        application_name = model_path_string_parts[5]
        model_name = "_".join(model_path_string_parts[3].split("#")[:2])
        route_prefix = f'/{model_name}/{model_path_string_parts[3].split("#")[3]}'
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

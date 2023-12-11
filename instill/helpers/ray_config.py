import argparse
from typing import Callable, Optional

import ray
from ray import serve
from ray.serve import Deployment
from ray.serve import deployment as ray_deployment

from instill.helpers.const import (
    DEFAULT_AUTOSCALING_CONFIG,
    DEFAULT_MAX_CONCURRENT_QUERIES,
    DEFAULT_RAY_ACTOR_OPRTIONS,
)


class InstillRayModelConfig:
    def __init__(
        self,
        ray_actor_options: dict,
        ray_autoscaling_options: dict,
        max_concurrent_queries: int,
        og_model_path: str,
        ray_addr: str,
    ) -> None:
        self.ray_addr = ray_addr

        og_model_string_parts = og_model_path.split("/")

        self.ray_actor_options = ray_actor_options
        self.ray_autoscaling_options = ray_autoscaling_options
        self.max_concurrent_queries = max_concurrent_queries

        self.model_path = og_model_path
        self.application_name = og_model_string_parts[5]
        self.model_name = "_".join(og_model_string_parts[3].split("#")[:2])
        self.route_prefix = (
            f'/{self.model_name}/{og_model_string_parts[3].split("#")[3]}'
        )


def get_compose_ray_address(port: int):
    return f"ray://ray_server:{port}"


def entry(model_weight_name_or_folder: str):
    parser = argparse.ArgumentParser()

    ray_actor_options = {
        "num_cpus": 1,
    }
    max_concurrent_queries = 10
    ray_autoscaling_options = {
        "target_num_ongoing_requests_per_replica": 7,
        "initial_replicas": 1,
        "min_replicas": 0,
        "max_replicas": 5,
    }

    parser.add_argument(
        "--func", required=True, choices=["deploy", "undeploy"], help="deploy/undeploy"
    )
    parser.add_argument("--model", required=True, help="model path for the deployment")
    parser.add_argument(
        "--ray-addr", default=get_compose_ray_address(10001), help="ray head address"
    )
    parser.add_argument(
        "--ray-actor-options",
        default=ray_actor_options,
        help="custom actor options for the deployment",
    )
    parser.add_argument(
        "--ray-autoscaling-options",
        default=ray_autoscaling_options,
        help="custom autoscaling options for the deployment",
    )
    args = parser.parse_args()

    ray_addr = "ray://" + args.ray_addr.replace("9000", "10001")

    model_config = InstillRayModelConfig(
        ray_addr=ray_addr,
        ray_actor_options=args.ray_actor_options,
        ray_autoscaling_options=args.ray_autoscaling_options,
        max_concurrent_queries=max_concurrent_queries,
        og_model_path="/".join([args.model, model_weight_name_or_folder]),
    )

    return args.func, model_config


class InstillDeployable:
    def __init__(
        self, deployable: Deployment, model_weight_or_folder_name: str
    ) -> None:
        self._deployment: Deployment = deployable
        # params
        self.model_weight_or_folder_name: str = model_weight_or_folder_name

    def update_num_cpus(self, num_cpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_cpus": num_cpus})

    def update_num_gpus(self, num_gpus: float):
        if self._deployment.ray_actor_options is not None:
            self._deployment.ray_actor_options.update({"num_gpus": num_gpus})

    def deploy(self, model_folder_path: str, ray_addr: str):
        if not ray.is_initialized():
            ray_addr = "ray://" + ray_addr.replace("9000", "10001")
            ray.init(ray_addr)
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
            ray.init(ray_addr)
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
    ray_actor_options = DEFAULT_RAY_ACTOR_OPRTIONS
    autoscaling_config = DEFAULT_AUTOSCALING_CONFIG
    max_concurrent_queries = DEFAULT_MAX_CONCURRENT_QUERIES

    return ray_deployment(
        _func_or_class=_func_or_class,
        ray_actor_options=ray_actor_options,
        autoscaling_config=autoscaling_config,
        max_concurrent_queries=max_concurrent_queries,
    )

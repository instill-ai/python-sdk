import argparse


class InstillRayModelConfig:
    def __init__(
        self,
        ray_actor_options: dict,
        ray_autoscaling_options: dict,
        max_concurrent_queries: int,
        og_model_path: str,
    ) -> None:
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


def get_cluster_ray_address(port: int):
    return f"ray://core_ray_server:{port}"


def entry(model_weight_name_or_folder: str):
    parser = argparse.ArgumentParser()

    ray_actor_options = {
        "num_cpus": 2,
    }
    max_concurrent_queries = 10
    ray_autoscaling_options = {
        "target_num_ongoing_requests_per_replica": 7,
        "initial_replicas": 0,
        "min_replicas": 0,
        "max_replicas": 5,
    }

    parser.add_argument(
        "--func", required=True, choices=["deploy", "undeploy"], help="deploy/undeploy"
    )
    parser.add_argument("--model", required=True, help="model path for the deployment")
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

    model_config = InstillRayModelConfig(
        ray_actor_options=args.ray_actor_options,
        ray_autoscaling_options=args.ray_autoscaling_options,
        max_concurrent_queries=max_concurrent_queries,
        og_model_path="/".join([args.model, model_weight_name_or_folder]),
    )

    return args.func, model_config

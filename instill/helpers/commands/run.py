"""Run command for the Instill CLI."""

import subprocess
import uuid

from instill.utils.logger import Logger

from .utils import BASH_SCRIPT, parse_image_tag_name


def add_run_parser(subcommands):
    """Add run command parser to subcommands."""
    run_parser = subcommands.add_parser("run", help="Run inference on model image")
    run_parser.set_defaults(func=run)
    run_parser.add_argument(
        "name",
        help="""
            Image name and tag for the model with the format <namespace>/<model>[:tag]
            (default tag is 'latest')
        """,
    )
    run_parser.add_argument(
        "-nc",
        "--num-of-cpus",
        help="Number of CPUs to use if --gpu flag is off, default to 1",
        type=int,
        default=1,
        required=False,
    )
    run_parser.add_argument(
        "-cs",
        "--cpu-kvcache-space",
        help="CPU KV-Cache space in GB. If not specified, default to 4GB",
        type=int,
        default=4,
        required=False,
    )
    run_parser.add_argument(
        "-g",
        "--gpu",
        help="Whether the model runs on GPUs",
        action="store_true",
        required=False,
    )
    run_parser.add_argument(
        "-ng",
        "--num-of-gpus",
        help="Number of GPUs to use if --gpu flag is on, default to 1",
        type=int,
        default=1,
        required=False,
    )
    run_parser.add_argument(
        "-i",
        "--input",
        help="Inference input as a string in JSON format",
        type=str,
        required=True,
    )


def run(args):
    """Run inference on a model image."""
    docker_run = False
    try:
        name = uuid.uuid4()
        image_name_tag = parse_image_tag_name(args.name)
        Logger.i("[Instill] Starting model image...")
        if not args.gpu:
            subprocess.run(
                [
                    "docker",
                    "run",
                    "-d",
                    "--privileged",
                    "--shm-size=4gb",
                    "--rm",
                    "-e",
                    f"VLLM_CPU_OMP_THREADS_BIND=0-{args.num_of_cpus}",
                    "-e",
                    f"VLLM_CPU_KVCACHE_SPACE={args.cpu_kvcache_space}",
                    "--name",
                    str(name),
                    image_name_tag,
                    "serve",
                    "run",
                    "_model:entrypoint",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        else:
            subprocess.run(
                [
                    "docker",
                    "run",
                    "-d",
                    "--privileged",
                    "--shm-size=4gb",
                    "--rm",
                    "--name",
                    str(name),
                    "--device",
                    f"nvidia.com/gpu:{args.num_of_gpus}",
                    f"{image_name_tag}",
                    "/bin/bash",
                    "-c",
                    "serve build _model:entrypoint -o serve.yaml && "
                    f"sed -i 's/app1/default/' serve.yaml && "
                    f"sed -i 's/num_cpus: 0.0/num_gpus: {args.num_of_gpus}/' serve.yaml && "
                    "serve run serve.yaml",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        docker_run = True
        subprocess.run(
            f"docker exec {str(name)} /bin/bash -c '{BASH_SCRIPT}'",
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            timeout=300,
        )

        Logger.i("[Instill] Deploying model...")
        subprocess.run(
            [
                "docker",
                "exec",
                str(name),
                "/bin/bash",
                "-c",
                "until serve status --name default | grep 'RUNNING: 1' > /dev/null; do sleep 1; done;",
            ],
            check=True,
        )
        Logger.i("[Instill] Running inference...")
        subprocess.run(
            [
                "docker",
                "exec",
                str(name),
                "python",
                "-m",
                "instill.helpers.test",
                "-i",
                args.input,
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        Logger.e("[Instill] Run failed")
    except subprocess.TimeoutExpired:
        Logger.e("[Instill] Deployment timeout")
    except (RuntimeError, OSError, IOError) as e:
        Logger.e("[Instill] Prepare failed")
        Logger.e(e)
    finally:
        if docker_run:
            subprocess.run(
                [
                    "docker",
                    "stop",
                    str(name),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        Logger.i("[Instill] Done")

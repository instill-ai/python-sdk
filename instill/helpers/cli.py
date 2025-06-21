import argparse

# import hashlib
import os
import platform
import shutil
import subprocess
import tempfile
import uuid

import ray
import yaml

import instill
from instill.helpers.errors import ModelConfigException
from instill.utils.logger import Logger

from instill.helpers.const import (
    PYTHON_VERSION_MIN,
    PYTHON_VERSION_MAX,
    CUDA_VERSION_MIN,
    CUDA_VERSION_MAX,
    TRANSFORMERS_VERSION,
    VLLM_VERSION,
    MLC_LLM_VERSION,
)

BASH_SCRIPT = """
until curl -s -o /dev/null -w "%{http_code}" http://localhost:8265 | grep -q "200"; do
    sleep 5
done
"""


def config_check_required_fields(c):
    """Check if required fields are present in the model configuration."""
    if "build" not in c or c["build"] is None:
        raise ModelConfigException("build")
    if "gpu" not in c["build"] or c["build"]["gpu"] is None:
        raise ModelConfigException("gpu")

def cli():
    """Command line interface for the Instill CLI tool."""
    if platform.machine() in ("i386", "AMD64", "x86_64"):
        default_platform = "amd64"
    else:
        default_platform = platform.machine()
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(required=True)

    # init
    init_parser = subcommands.add_parser("init", help="Initialize model directory")
    init_parser.set_defaults(func=init)

    # build
    build_parser = subcommands.add_parser("build", help="Build model image")
    build_parser.set_defaults(func=build)
    build_parser.add_argument(
        "name",
        help="""
            Image name and tag for the model with the format <namespace>/<model>[:tag]
            (default tag is 'latest')
        """,
    )
    build_parser.add_argument(
        "-n",
        "--no-cache",
        help="Build the image without cache",
        default=False,
        action="store_true",
        required=False,
    )
    build_parser.add_argument(
        "-a",
        "--target-arch",
        help="Target platform architecture for the model image. If not specified, default to host architecture",
        default=default_platform,
        choices=["arm64", "amd64"],
        required=False,
    )
    build_parser.add_argument(
        "-w",
        "--sdk-wheel",
        help="The python-sdk wheel absolute path",
        default=None,
        required=False,
    )
    build_parser.add_argument(
        "-e",
        "--editable-project",
        help="""
            The python-sdk project path to install in editable mode
            (overrides --sdk-wheel if both are specified)
        """,
        default=None,
        required=False,
    )

    # push
    push_parser = subcommands.add_parser("push", help="Push model image")
    push_parser.set_defaults(func=push)
    push_parser.add_argument(
        "name",
        help="""
            Image name and tag for the model with the format <namespace>/<model>[:tag]
            (default tag is 'latest')
        """,
    )
    push_parser.add_argument(
        "-u",
        "--url",
        help="Image registry URL in the format of host:port. If not specified, default to api.instill-ai.com",
        default="api.instill-ai.com",
        required=False,
    )

    # run
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

    args = parser.parse_args()
    args.func(args)


def init(_):
    """Initialize a new model directory with template files."""
    shutil.copyfile(
        __file__.replace("cli.py", "init-templates/instill.yaml"),
        f"{os.getcwd()}/instill.yaml",
    )
    shutil.copyfile(
        __file__.replace("cli.py", "init-templates/model.py"),
        f"{os.getcwd()}/model.py",
    )


def find_project_root(start_path):
    """Find the Python project root by looking for setup.py or pyproject.toml"""
    current_path = os.path.abspath(start_path)
    while current_path != "/":
        if os.path.exists(os.path.join(current_path, "setup.py")) or os.path.exists(
            os.path.join(current_path, "pyproject.toml")
        ):
            return current_path
        current_path = os.path.dirname(current_path)
    return None

def validate_python_version(python_version: str) -> str:
    """Validate Python version and return cleaned version string."""
    # Set default Python version if not provided
    if not python_version:
        python_version = "3.11"

    # Validate Python version format first
    try:
        version_parts = [int(x) for x in python_version.split(".")]
        if len(version_parts) < 2:
            raise ValueError(f"Invalid Python version format: {python_version}. Must be in format X.Y (e.g., 3.11)")
    except (ValueError, IndexError) as exc:
        raise ValueError(f"Invalid Python version format: {python_version}. Must be in format X.Y (e.g., 3.11)") from exc

    # Then validate version range
    major, minor = version_parts[0], version_parts[1]

    # Parse min and max versions
    min_major, min_minor = map(int, PYTHON_VERSION_MIN.split('.'))
    max_major, max_minor = map(int, PYTHON_VERSION_MAX.split('.'))

    # Compare major version first, then minor version
    if major < min_major or (major == min_major and minor < min_minor):
        raise ValueError(f"Python version {python_version} is too old. Must be at least {PYTHON_VERSION_MIN}")

    if major > max_major or (major == max_major and minor > max_minor):
        raise ValueError(f"Python version {python_version} is too new. Must be at most {PYTHON_VERSION_MAX}")

    return python_version.replace(".", "")


def validate_cuda_version(cuda_version: str) -> str:
    """Validate CUDA version and return cleaned version string."""
    # Set default CUDA version if not provided
    if not cuda_version:
        cuda_version = "12.8"

    # Validate CUDA version format first
    try:
        version_parts = [int(x) for x in cuda_version.split(".")]
        if len(version_parts) < 2:
            raise ValueError(f"Invalid CUDA version format: {cuda_version}. Must be in format X.Y (e.g., 12.8)")
    except (ValueError, IndexError) as exc:
        raise ValueError(f"Invalid CUDA version format: {cuda_version}. Must be in format X.Y (e.g., 12.8)") from exc

    # Then validate version range
    major, minor = version_parts[0], version_parts[1]

    # Parse min and max versions
    min_major, min_minor = map(int, CUDA_VERSION_MIN.split('.'))
    max_major, max_minor = map(int, CUDA_VERSION_MAX.split('.'))

    # Compare major version first, then minor version
    if major < min_major or (major == min_major and minor < min_minor):
        raise ValueError(f"CUDA version {cuda_version} is too old. Must be at least {CUDA_VERSION_MIN}")

    if major > max_major or (major == max_major and minor > max_minor):
        raise ValueError(f"CUDA version {cuda_version} is too new. Must be at most {CUDA_VERSION_MAX}")

    return cuda_version.replace(".", "")


def prepare_build_environment(build_params):
    """Prepare environment variables and settings for the build process."""

    # Prepare Ray version
    ray_version = ray.__version__

    # Prepare Python version
    python_version = f"-py{validate_python_version(build_params.get('python_version'))}"

    # Prepare CUDA version and device type
    if not build_params["gpu"]:
        cuda_version = ""
        device_type = "-cpu"
    elif build_params.get("cuda_version") is not None:
        cuda_version = f'-cu{validate_cuda_version(build_params["cuda_version"])}'
        device_type = "-gpu"
    else:
        cuda_version = "-cu128"  # Default to 12.8
        device_type = "-gpu"

    llm_runtime = build_params.get("llm_runtime")

    # Prepare system packages
    system_pkg_list = []
    if (
        "system_packages" in build_params
        and not build_params["system_packages"] is None
    ):
        system_pkg_list.extend(build_params["system_packages"])
    system_pkg_str = " ".join(system_pkg_list)

    # Prepare Python packages
    python_pkg_list = []
    if (
        "python_packages" in build_params
        and build_params["python_packages"] is not None
    ):
        python_pkg_list.extend(build_params["python_packages"])
    python_pkg_str = " ".join(python_pkg_list)

    # Prepare Instill SDK version
    instill_sdk_version = instill.__version__

    return (
        llm_runtime,
        ray_version,
        python_version,
        cuda_version,
        device_type,
        system_pkg_str,
        python_pkg_str,
        instill_sdk_version,
    )

def parse_image_tag_name(image_tag_name: str):
    """Parse image name to extract name and tag."""
    if ":" in image_tag_name:
        return image_tag_name
    return f"{image_tag_name}:latest"


def parse_target_arch(target_arch: str):
    """Parse target architecture."""
    if target_arch not in ["amd64", "arm64"]:
        raise ValueError(f"Invalid target architecture: {target_arch}. Must be 'amd64' or 'arm64'")

    if target_arch == "arm64":
        return "aarch64"
    return "amd64"


def prepare_build_command(tmpdir, dockerfile, build_vars):
    """Prepare the Docker build command with all necessary arguments."""
    (
        image_name_tag,
        target_arch,
        no_cache,
        llm_runtime,
        ray_version,
        python_version,
        cuda_version,
        device_type,
        python_pkg_str,
        system_pkg_str,
        instill_sdk_version,
        instill_python_sdk_project_name,
    ) = build_vars

    command = [
        "docker",
        "buildx",
        "build",
        "--progress=plain",
        "--file",
        f"{tmpdir}/{dockerfile}",
        "--build-arg",
        f"RAY_VERSION={ray_version}",
        "--build-arg",
        f"PYTHON_VERSION={python_version}",
        "--build-arg",
        f"CUDA_VERSION={cuda_version}",
        "--build-arg",
        f"DEVICE_TYPE={device_type}",
        "--build-arg",
        f"PYTHON_PACKAGES={python_pkg_str}",
        "--build-arg",
        f"INSTILL_PYTHON_SDK_VERSION={instill_sdk_version}",
        "--platform",
        f"linux/{target_arch}",
        "-t",
        f"{image_name_tag}",
        tmpdir,
        "--load",
    ]

    # Add conditional build args
    if no_cache:
        command.append("--no-cache")

    # Extract LLM runtime version
    if "mlc-llm" in llm_runtime:
        llm_runtime_version = llm_runtime.split("==")[1] if "==" in llm_runtime else MLC_LLM_VERSION
        command.extend(["--build-arg", f"MLC_LLM_VERSION={llm_runtime_version}"])
    elif "vllm" in llm_runtime:
        llm_runtime_version = llm_runtime.split("==")[1] if "==" in llm_runtime else VLLM_VERSION
        command.extend(["--build-arg", f"VLLM_VERSION={llm_runtime_version}"])
    elif "transformers" in llm_runtime:
        llm_runtime_version = llm_runtime.split("==")[1] if "==" in llm_runtime else TRANSFORMERS_VERSION
        command.extend(["--build-arg", f"TRANSFORMERS_VERSION={llm_runtime_version}"])

    if system_pkg_str:
        command.extend(["--build-arg", f"SYSTEM_PACKAGES={system_pkg_str}"])

    command.extend(
        [
            # editable mode
            "--build-arg",
            f"INSTILL_PYTHON_SDK_PROJECT_NAME={instill_python_sdk_project_name}",
            "--build-arg",
            (
                "PYTHONPATH_USER_DEFINED_PROTO=/home/ray/"
                f"{instill_python_sdk_project_name}/instill/protogen/model/ray/v1alpha"
            ),
        ]
        if instill_python_sdk_project_name
        else [
            "--build-arg",
            (
                "PYTHONPATH_USER_DEFINED_PROTO=/home/ray/"
                f"anaconda3/lib/python3.{python_version[4:]}/"
                "site-packages/instill/protogen/model/ray/v1alpha"
            ),
        ]
    )

    return command


def build(args):
    """Build a Docker image for the model with specified configuration."""
    try:
        Logger.i("[Instill] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill] Parsing config file...")
            config = yaml.safe_load(f)

        config_check_required_fields(config)
        build_params = config["build"]

        if build_params.get("gpu") and args.target_arch == "arm64":
            raise ValueError("GPU is not supported on ARM64 architecture")

        # Prepare build environment
        (
            llm_runtime,
            ray_version,
            python_version,
            cuda_version,
            device_type,
            system_pkg_str,
            python_pkg_str,
            instill_sdk_version,
        ) = prepare_build_environment(build_params)

        if "mlc-llm" in llm_runtime:
            dockerfile = "Dockerfile.mlc-llm"
        elif "vllm" in llm_runtime:
            dockerfile = "Dockerfile.vllm"
        elif "transformers" in llm_runtime:
            dockerfile = "Dockerfile.transformers"
        else:
            dockerfile = "Dockerfile"

        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy files to tmpdir
            docker_dir = __file__.replace("cli.py", "docker")
            shutil.copyfile(f"{docker_dir}/{dockerfile}", f"{tmpdir}/{dockerfile}")
            shutil.copyfile(f"{docker_dir}/.dockerignore", f"{tmpdir}/.dockerignore")
            shutil.copytree(
                os.getcwd(),
                tmpdir,
                ignore=shutil.ignore_patterns("model.py"),
                dirs_exist_ok=True,
            )
            shutil.copyfile(f"{os.getcwd()}/model.py", f"{tmpdir}/_model.py")

            # Handle SDK wheel if provided
            if args.sdk_wheel is not None:
                shutil.copyfile(
                    args.sdk_wheel,
                    f"{tmpdir}/instill_sdk-{instill_sdk_version}dev-py3-none-any.whl",
                )

            # Handle editable project installation
            instill_sdk_project_name = None
            if args.editable_project:
                project_root = find_project_root(args.editable_project)
                if project_root is None:
                    raise FileNotFoundError("""
                    [Instill] No Python project found at the specified path (missing setup.py or pyproject.toml)
                    """)
                instill_sdk_project_name = os.path.basename(project_root)
                Logger.i(f"[Instill] Found Python project: {instill_sdk_project_name}")
                shutil.copytree(
                    project_root,
                    f"{tmpdir}/{instill_sdk_project_name}",
                    dirs_exist_ok=True,
                )

            Logger.i("[Instill] Building model image...")
            image_name_tag = parse_image_tag_name(args.name)
            target_arch = parse_target_arch(args.target_arch)
            build_vars = [
                image_name_tag,
                target_arch,
                args.no_cache,
                llm_runtime,
                ray_version,
                python_version,
                cuda_version,
                device_type,
                python_pkg_str,
                system_pkg_str,
                instill_sdk_version,
                instill_sdk_project_name,
            ]
            command = prepare_build_command(tmpdir, dockerfile, build_vars)

            subprocess.run(command, check=True)
            Logger.i(f"[Instill] {image_name_tag} built")
    except subprocess.CalledProcessError:
        Logger.e("[Instill] Build failed")
    except (ValueError, FileNotFoundError, OSError, IOError) as e:
        Logger.e("[Instill] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill] Done")


def push(args):
    """Push a built model image to a Docker registry."""
    registry = args.url
    image_name_tag = parse_image_tag_name(args.name)
    tagged_image = f"{registry}/{image_name_tag}"
    try:
        # Tag the image
        subprocess.run(
            [
                "docker",
                "tag",
                f"{image_name_tag}",
                tagged_image,
            ],
            check=True,
        )
        Logger.i("[Instill] Pushing model image...")
        # Push the image
        subprocess.run(["docker", "push", tagged_image], check=True)
        Logger.i(f"[Instill] {tagged_image} pushed")
    except subprocess.CalledProcessError:
        Logger.e("[Instill] Push failed")
    except (ConnectionError, OSError, IOError) as e:
        Logger.e("[Instill] Prepare failed")
        Logger.e(e)
    finally:
        # Remove the tagged image regardless of success/failure
        try:
            subprocess.run(
                ["docker", "rmi", tagged_image],
                check=True,
            )
        except subprocess.CalledProcessError:
            Logger.e(f"[Instill] Failed to remove tagged image {tagged_image}")
        Logger.i("[Instill] Done")


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


if __name__ == "__main__":
    cli()

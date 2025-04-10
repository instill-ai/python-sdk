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
from instill.helpers.const import DEFAULT_DEPENDENCIES
from instill.helpers.errors import ModelConfigException
from instill.utils.logger import Logger

bash_script = """
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
    if "python_version" not in c["build"] or c["build"]["python_version"] is None:
        raise ModelConfigException("python_version")


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
        help="user and model namespace, in the format of <user-id>/<model-id>[:tag] (default tag is 'latest')",
    )
    build_parser.add_argument(
        "-n",
        "--no-cache",
        help="build the image without cache",
        action="store_true",
        required=False,
    )
    build_parser.add_argument(
        "-a",
        "--target-arch",
        help="target platform architecture for the model image, default to host",
        default=default_platform,
        choices=["arm64", "amd64"],
        required=False,
    )
    build_parser.add_argument(
        "-w",
        "--sdk-wheel",
        help="instill sdk wheel absolute path for debug purpose",
        default=None,
        required=False,
    )
    build_parser.add_argument(
        "-e",
        "--editable-project",
        help="path to local Python project to install in editable mode (overrides --sdk-wheel if both are specified)",
        default=None,
        required=False,
    )

    # push
    push_parser = subcommands.add_parser("push", help="Push model image")
    push_parser.set_defaults(func=push)
    push_parser.add_argument(
        "name",
        help="user and model namespace, in the format of <user-id>/<model-id>[:tag] (default tag is 'latest')",
    )
    push_parser.add_argument(
        "-u",
        "--url",
        help="image registry url, in the format of host:port, default to api.instill.tech",
        default="api.instill.tech",
        required=False,
    )

    # run
    run_parser = subcommands.add_parser("run", help="Run inference on model image")
    run_parser.set_defaults(func=run)
    run_parser.add_argument(
        "name",
        help="user and model namespace, in the format of <user-id>/<model-id>[:tag] (default tag is 'latest')",
    )
    run_parser.add_argument(
        "-g",
        "--gpu",
        help="whether the model needs gpu",
        action="store_true",
        required=False,
    )
    run_parser.add_argument(
        "-ng",
        "--num-of-gpus",
        help="number of gpus to use if gpu flag is on, default to 1",
        type=int,
        default=1,
        required=False,
    )
    run_parser.add_argument(
        "-i",
        "--input",
        help="inference input json",
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
    shutil.copyfile(
        __file__.replace("cli.py", "init-templates/.dockerignore"),
        f"{os.getcwd()}/.dockerignore",
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


def is_vllm_version_compatible(version_parts):
    """Check if vLLM version meets minimum requirements (v0.6.5)"""
    return not (
        version_parts[0] < 0
        or (version_parts[0] == 0 and version_parts[1] < 6)
        or (version_parts[0] == 0 and version_parts[1] == 6 and version_parts[2] < 5)
    )


def prepare_build_environment(build_params):
    """Prepare environment variables and settings for the build process."""
    python_version = build_params["python_version"].replace(".", "")
    ray_version = ray.__version__
    instill_sdk_version = instill.__version__

    # Determine CUDA suffix
    if not build_params["gpu"]:
        cuda_suffix = ""
    elif "cuda_version" in build_params and not build_params["cuda_version"] is None:
        cuda_suffix = f'-cu{build_params["cuda_version"].replace(".", "")}'
    else:
        cuda_suffix = "-gpu"

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
    python_pkg_list.extend(DEFAULT_DEPENDENCIES)

    return (
        python_version,
        ray_version,
        instill_sdk_version,
        cuda_suffix,
        system_pkg_str,
        python_pkg_list,
    )


def process_arm64_packages(python_pkg_list, target_arch):
    """Process packages for ARM64 architecture, handling vLLM and other dependencies."""
    dockerfile = "Dockerfile"
    vllm_version = None

    if target_arch == "arm64":
        filtered_pkg_list = []
        for pkg in python_pkg_list:
            if pkg.startswith("vllm"):
                # Transform version string from "0.6.4.post1" to "v0.6.4"
                version = pkg.split("==")[1]
                vllm_version = f"v{version.split('.post')[0]}"
                # Check if version is at least v0.6.5
                base_version = version.split(".post")[0]
                version_parts = [int(x) for x in base_version.split(".")]
                if not is_vllm_version_compatible(version_parts):
                    raise ValueError(
                        f"[Instill] vLLM version must be at least v0.6.5, got {vllm_version}"
                    )
            elif pkg.startswith("bitsandbytes"):
                raise ValueError(
                    "[Instill] bitsandbytes is not supported on ARM architecture"
                )
            else:
                filtered_pkg_list.append(pkg)

        python_pkg_list = filtered_pkg_list
        if vllm_version is not None:
            dockerfile = "Dockerfile.arm"

    python_pkg_str = " ".join(python_pkg_list)
    target_arch_suffix = "-aarch64" if target_arch == "arm64" else ""

    return dockerfile, vllm_version, python_pkg_str, target_arch_suffix, python_pkg_list


def parse_image_name(name):
    """Parse image name to extract name and tag."""
    if ":" in name:
        image, tag = name.split(":", 1)
        return image, tag
    return name, "latest"


def prepare_build_command(args, tmpdir, dockerfile, build_vars):
    """Prepare the Docker build command with all necessary arguments."""
    vllm_version, target_arch_suffix, ray_version, python_version = build_vars[:4]
    cuda_suffix, python_pkg_str, system_pkg_str, instill_sdk_version = build_vars[4:8]
    instill_python_sdk_project_name = build_vars[8]

    image_name, tag = parse_image_name(args.name)

    command = [
        "docker",
        "buildx",
        "build",
        "--progress=plain",
        "--file",
        f"{tmpdir}/{dockerfile}",
        "--build-arg",
        f"TARGET_ARCH_SUFFIX={target_arch_suffix}",
        "--build-arg",
        f"RAY_VERSION={ray_version}",
        "--build-arg",
        f"PYTHON_VERSION={python_version}",
        "--build-arg",
        f"PYTHON_PACKAGES={python_pkg_str}",
        "--build-arg",
        f"INSTILL_PYTHON_SDK_VERSION={instill_sdk_version}",
        "--platform",
        f"linux/{args.target_arch}",
        "-t",
        f"{image_name}:{tag}",
        tmpdir,
        "--load",
    ]

    # Add conditional build args
    if args.no_cache:
        command.append("--no-cache")

    if vllm_version:
        command.extend(["--build-arg", f"VLLM_VERSION={vllm_version}"])

    if cuda_suffix:
        command.extend(["--build-arg", f"CUDA_SUFFIX={cuda_suffix}"])

    if system_pkg_str:
        command.extend(["--build-arg", f"SYSTEM_PACKAGES={system_pkg_str}"])

    command.extend(
        [
            "--build-arg",
            f"INSTILL_PYTHON_SDK_PROJECT_NAME={instill_python_sdk_project_name}",
        ]
        if instill_python_sdk_project_name
        else []
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

        # Prepare build environment
        (
            python_version,
            ray_version,
            instill_sdk_version,
            cuda_suffix,
            system_pkg_str,
            python_pkg_list,
        ) = prepare_build_environment(build_params)

        # Process ARM64-specific packages
        (
            dockerfile,
            vllm_version,
            python_pkg_str,
            target_arch_suffix,
            python_pkg_list,
        ) = process_arm64_packages(python_pkg_list, args.target_arch)

        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy files to tmpdir
            shutil.copyfile(
                __file__.replace("cli.py", f"docker/{dockerfile}"),
                f"{tmpdir}/{dockerfile}",
            )
            shutil.copytree(os.getcwd(), tmpdir, dirs_exist_ok=True)

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
                    raise FileNotFoundError(
                        "[Instill] No Python project found at the specified path (missing setup.py or pyproject.toml)"
                    )
                instill_sdk_project_name = os.path.basename(project_root)
                Logger.i(f"[Instill] Found Python project: {instill_sdk_project_name}")
                shutil.copytree(
                    project_root,
                    f"{tmpdir}/{instill_sdk_project_name}",
                    dirs_exist_ok=True,
                )

            Logger.i("[Instill] Building model image...")
            build_vars = [
                vllm_version,
                target_arch_suffix,
                ray_version,
                python_version,
                cuda_suffix,
                python_pkg_str,
                system_pkg_str,
                instill_sdk_version,
                instill_sdk_project_name,
            ]
            command = prepare_build_command(args, tmpdir, dockerfile, build_vars)

            subprocess.run(command, check=True)
            image_name, tag = parse_image_name(args.name)
            Logger.i(f"[Instill] {image_name}:{tag} built")
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
    image_name, tag = parse_image_name(args.name)
    tagged_image = f"{registry}/{image_name}:{tag}"
    try:
        # Tag the image
        subprocess.run(
            [
                "docker",
                "tag",
                f"{image_name}:{tag}",
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
        image_name, tag = parse_image_name(args.name)
        Logger.i("[Instill] Starting model image...")
        if not args.gpu:
            subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-d",
                    "--shm-size=4gb",
                    "--name",
                    str(name),
                    f"{image_name}:{tag}",
                    "serve",
                    "run",
                    "_model:entrypoint",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        else:
            subprocess.run(
                f"docker run \
                    --rm -d --shm-size=4gb --name {str(name)} --gpus all \
                    {image_name}:{tag} /bin/bash -c \
                        \"serve build _model:entrypoint -o serve.yaml && \
                        sed -i 's/app1/default/' serve.yaml && \
                        sed -i 's/num_cpus: 0.0/num_gpus: {args.num_of_gpus}/' serve.yaml && \
                        serve run serve.yaml\"",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
        docker_run = True
        subprocess.run(
            f"docker exec {str(name)} /bin/bash -c '{bash_script}'",
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

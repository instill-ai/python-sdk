"""Shared utilities for CLI commands."""

import os

import ray

import instill
from instill.helpers.const import (
    CUDA_VERSION_MAX,
    CUDA_VERSION_MIN,
    MLC_LLM_VERSION,
    PYTHON_VERSION_MAX,
    PYTHON_VERSION_MIN,
    TRANSFORMERS_VERSION,
    VLLM_VERSION,
)
from instill.helpers.errors import ModelConfigException

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
        python_version = "3.12"

    # Validate Python version format first
    try:
        version_parts = [int(x) for x in python_version.split(".")]
        if len(version_parts) < 2:
            raise ValueError(
                f"Invalid Python version format: {python_version}. Must be in format X.Y (e.g., 3.12)"
            )
    except (ValueError, IndexError) as exc:
        raise ValueError(
            f"Invalid Python version format: {python_version}. Must be in format X.Y (e.g., 3.12)"
        ) from exc

    # Then validate version range
    major, minor = version_parts[0], version_parts[1]

    # Parse min and max versions
    min_major, min_minor = map(int, PYTHON_VERSION_MIN.split("."))
    max_major, max_minor = map(int, PYTHON_VERSION_MAX.split("."))

    # Compare major version first, then minor version
    if major < min_major or (major == min_major and minor < min_minor):
        raise ValueError(
            f"Python version {python_version} is too old. Must be at least {PYTHON_VERSION_MIN}"
        )

    if major > max_major or (major == max_major and minor > max_minor):
        raise ValueError(
            f"Python version {python_version} is too new. Must be at most {PYTHON_VERSION_MAX}"
        )

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
            raise ValueError(
                f"Invalid CUDA version format: {cuda_version}. Must be in format X.Y (e.g., 12.8)"
            )
    except (ValueError, IndexError) as exc:
        raise ValueError(
            f"Invalid CUDA version format: {cuda_version}. Must be in format X.Y (e.g., 12.8)"
        ) from exc

    # Then validate version range
    major, minor = version_parts[0], version_parts[1]

    # Parse min and max versions
    min_major, min_minor = map(int, CUDA_VERSION_MIN.split("."))
    max_major, max_minor = map(int, CUDA_VERSION_MAX.split("."))

    # Compare major version first, then minor version
    if major < min_major or (major == min_major and minor < min_minor):
        raise ValueError(
            f"CUDA version {cuda_version} is too old. Must be at least {CUDA_VERSION_MIN}"
        )

    if major > max_major or (major == max_major and minor > max_minor):
        raise ValueError(
            f"CUDA version {cuda_version} is too new. Must be at most {CUDA_VERSION_MAX}"
        )

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
        raise ValueError(
            f"Invalid target architecture: {target_arch}. Must be 'amd64' or 'arm64'"
        )

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
    if llm_runtime is not None:
        if "mlc-llm" in llm_runtime:
            llm_runtime_version = (
                llm_runtime.split("==")[1] if "==" in llm_runtime else MLC_LLM_VERSION
            )
            command.extend(["--build-arg", f"MLC_LLM_VERSION={llm_runtime_version}"])
        elif "vllm" in llm_runtime:
            llm_runtime_version = (
                llm_runtime.split("==")[1] if "==" in llm_runtime else VLLM_VERSION
            )
            command.extend(["--build-arg", f"VLLM_VERSION={llm_runtime_version}"])
        elif "transformers" in llm_runtime:
            llm_runtime_version = (
                llm_runtime.split("==")[1]
                if "==" in llm_runtime
                else TRANSFORMERS_VERSION
            )
            command.extend(
                ["--build-arg", f"TRANSFORMERS_VERSION={llm_runtime_version}"]
            )

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

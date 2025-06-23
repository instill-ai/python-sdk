"""Build command for the Instill CLI."""

import os
import shutil
import subprocess
import tempfile

import yaml

from instill.utils.logger import Logger

from .utils import (
    config_check_required_fields,
    find_project_root,
    parse_image_tag_name,
    parse_target_arch,
    prepare_build_command,
    prepare_build_environment,
)


def add_build_parser(subcommands, default_platform):
    """Add build command parser to subcommands."""
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

        dockerfile = "Dockerfile"
        if llm_runtime is not None:
            if "mlc-llm" in llm_runtime:
                dockerfile = "Dockerfile.mlc-llm"
            elif "vllm" in llm_runtime:
                dockerfile = "Dockerfile.vllm"
            elif "transformers" in llm_runtime:
                dockerfile = "Dockerfile.transformers"

        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy files to tmpdir
            docker_dir = __file__.replace("commands/build.py", "docker")
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
                    raise FileNotFoundError(
                        """
                    [Instill] No Python project found at the specified path (missing setup.py or pyproject.toml)
                    """
                    )
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
        Logger.e(str(e))
    finally:
        Logger.i("[Instill] Done")

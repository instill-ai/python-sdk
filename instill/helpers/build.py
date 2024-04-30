import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import tempfile

import ray
import yaml

import instill
from instill.helpers.const import DEFAULT_DEPENDENCIES
from instill.helpers.errors import ModelConfigException
from instill.utils.logger import Logger


def config_check_required_fields(c):
    if "build" not in c or c["build"] is None:
        raise ModelConfigException("build")
    if "gpu" not in c["build"] or c["build"]["gpu"] is None:
        raise ModelConfigException("gpu")
    if "python_version" not in c["build"] or c["build"]["python_version"] is None:
        raise ModelConfigException("python_version")
    if "repo" not in c or c["repo"] is None:
        raise ModelConfigException("repo")


def build_image():
    if platform.machine() in ("i386", "AMD64", "x86_64"):
        default_platform = "amd64"
    else:
        default_platform = platform.machine()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--tag",
        help="tag for the model image",
        default="",
        required=False,
    )
    parser.add_argument(
        "--no-cache",
        help="build the image without cache",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--target-arch",
        help="target platform architecture for the model image, default to host",
        default=default_platform,
        choices=["arm64", "amd64"],
        required=False,
    )

    args = parser.parse_args()
    try:
        Logger.i("[Instill Builder] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill Builder] Parsing config file...")
            config = yaml.safe_load(f)

        config_check_required_fields(config)

        build = config["build"]
        repo = config["repo"]
        tag = args.tag if args.tag != "" else hashlib.sha256().hexdigest()

        python_version = build["python_version"].replace(".", "")
        ray_version = ray.__version__
        instill_version = instill.__version__

        cuda_suffix = "" if not build["gpu"] else "-cu121"

        system_str = ""
        if "system_packages" in build and not build["system_packages"] is None:
            for p in build["system_packages"]:
                system_str += p + " "

        packages_str = ""
        if "python_packages" in build and not build["python_packages"] is None:
            for p in build["python_packages"]:
                packages_str += p + " "
        for p in DEFAULT_DEPENDENCIES:
            packages_str += p + " "
        packages_str += f"instill-sdk=={instill_version}"

        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copyfile(
                __file__.replace("build.py", "Dockerfile"), f"{tmpdir}/Dockerfile"
            )
            shutil.copyfile(
                __file__.replace("build.py", ".dockerignore"), f"{tmpdir}/.dockerignore"
            )
            shutil.copytree(os.getcwd(), tmpdir, dirs_exist_ok=True)

            target_arch_suffix = "-aarch64" if args.target_arch == "arm64" else ""

            Logger.i("[Instill Builder] Building model image...")
            command = [
                "docker",
                "buildx",
                "build",
                "--build-arg",
                f"TARGET_ARCH_SUFFIX={target_arch_suffix}",
                "--build-arg",
                f"RAY_VERSION={ray_version}",
                "--build-arg",
                f"PYTHON_VERSION={python_version}",
                "--build-arg",
                f"CUDA_SUFFIX={cuda_suffix}",
                "--build-arg",
                f"PACKAGES={packages_str}",
                "--build-arg",
                f"SYSTEM_PACKAGES={system_str}",
                "--platform",
                f"linux/{args.target_arch}",
                "-t",
                f"{repo}:{tag}",
                tmpdir,
                "--load",
            ]
            if args.no_cache:
                command.append("--no-cache")
            subprocess.run(
                command,
                check=True,
            )
            Logger.i(f"[Instill Builder] {repo}:{tag} built")
    except subprocess.CalledProcessError:
        Logger.e("[Instill Builder] Build failed")
    except Exception as e:
        Logger.e("[Instill Builder] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")


if __name__ == "__main__":
    build_image()

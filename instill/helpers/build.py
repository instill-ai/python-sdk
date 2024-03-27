import argparse
import hashlib
import os
import platform
import shutil
import tempfile

import docker
import ray
import yaml

import instill
from instill.helpers.const import DEFAULT_DEPENDENCIES
from instill.utils.logger import Logger

if __name__ == "__main__":
    Logger.i("[Instill Builder] Setup docker...")
    if platform.machine() in ("i386", "AMD64", "x86_64"):
        default_platform = "amd64"
    else:
        default_platform = platform.machine()
    parser = argparse.ArgumentParser()
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

    client = docker.from_env()
    try:
        args = parser.parse_args()

        Logger.i("[Instill Builder] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill Builder] Parsing config file...")
            config = yaml.safe_load(f)

        build = config["build"]
        repo = config["repo"]
        tag = (
            config["tag"]
            if config["tag"] is not None and config["tag"] != ""
            else hashlib.sha256().hexdigest()
        )

        python_version = build["python_version"].replace(".", "")
        ray_version = ray.__version__
        instill_version = instill.__version__

        cuda_suffix = "" if not build["gpu"] else "-cu121"

        packages_str = ""
        if not build["python_packages"] is None:
            for p in build["python_packages"]:
                packages_str += p + " "
        for p in DEFAULT_DEPENDENCIES:
            packages_str += p + " "
        packages_str += f"instill-sdk=={instill_version}"

        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copyfile(
                __file__.replace("build.py", "Dockerfile"), f"{tmpdir}/Dockerfile"
            )
            shutil.copytree(os.getcwd(), tmpdir, dirs_exist_ok=True)

            target_arch_suffix = "-aarch64" if args.target_arch == "arm64" else ""
            Logger.i("[Instill Builder] Building model image...")
            img, logs = client.images.build(
                path=tmpdir,
                rm=True,
                pull=True,
                nocache=args.no_cache,
                platform=f"linux/{args.target_arch}",
                tag=f"{repo}:{tag}",
                buildargs={
                    "TARGET_ARCH_SUFFIX": target_arch_suffix,
                    "RAY_VERSION": ray_version,
                    "PYTHON_VERSION": python_version,
                    "CUDA_SUFFIX": cuda_suffix,
                    "PACKAGES": packages_str,
                },
                quiet=False,
            )
            for line in logs:
                print(*line.values())
            Logger.i(f"[Instill Builder] {repo}:{tag} built")
    except Exception as e:
        Logger.e("[Instill Builder] Build failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")

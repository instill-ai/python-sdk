import argparse

# import hashlib
import os
import platform
import shutil
import subprocess
import tempfile
import time
import uuid

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


def cli():
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
        help="user and model namespace, in the format of <user-id>/<model-id>",
    )
    build_parser.add_argument(
        "-t",
        "--tag",
        help="tag for the model image, default to `latest`",
        # default=hashlib.sha256().hexdigest(),
        default="latest",
        required=False,
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

    # push
    push_parser = subcommands.add_parser("push", help="Push model image")
    push_parser.set_defaults(func=push)
    push_parser.add_argument(
        "name",
        help="user and model namespace, in the format of <user-id>/<model-id>",
    )
    push_parser.add_argument(
        "-u",
        "--url",
        help="image registry url, in the format of host:port, default to api.instill.tech",
        default="api.instill.tech",
        required=False,
    )
    push_parser.add_argument(
        "-t",
        "--tag",
        help="tag for the model image, default to `latest`",
        default="latest",
        required=False,
    )

    # run
    run_parser = subcommands.add_parser("run", help="Run inference on model image")
    run_parser.set_defaults(func=run)
    run_parser.add_argument(
        "name",
        help="user and model namespace, in the format of <user-id>/<model-id>",
    )
    run_parser.add_argument(
        "-t",
        "--tag",
        help="tag for the model image, default to `latest`",
        default="latest",
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


def build(args):
    try:
        Logger.i("[Instill Builder] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill Builder] Parsing config file...")
            config = yaml.safe_load(f)

        config_check_required_fields(config)

        build_params = config["build"]

        python_version = build_params["python_version"].replace(".", "")
        ray_version = ray.__version__
        instill_version = instill.__version__

        if not build_params["gpu"]:
            cuda_suffix = ""
        elif (
            "cuda_version" in build_params and not build_params["cuda_version"] is None
        ):
            cuda_suffix = f'-cu{build_params["cuda_version"].replace(".", "")}'
        else:
            cuda_suffix = "-gpu"

        system_str = ""
        if (
            "system_packages" in build_params
            and not build_params["system_packages"] is None
        ):
            for p in build_params["system_packages"]:
                system_str += p + " "

        packages_str = ""
        if (
            "python_packages" in build_params
            and not build_params["python_packages"] is None
        ):
            for p in build_params["python_packages"]:
                packages_str += p + " "
        for p in DEFAULT_DEPENDENCIES:
            packages_str += p + " "

        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copyfile(
                __file__.replace("cli.py", "init-templates/Dockerfile"),
                f"{tmpdir}/Dockerfile",
            )
            shutil.copytree(os.getcwd(), tmpdir, dirs_exist_ok=True)

            if args.sdk_wheel is not None:
                shutil.copyfile(
                    args.sdk_wheel,
                    f"{tmpdir}/instill_sdk-{instill_version}dev-py3-none-any.whl",
                )

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
                "--build-arg",
                f"SDK_VERSION={instill_version}",
                "--platform",
                f"linux/{args.target_arch}",
                "-t",
                f"{args.name}:{args.tag}",
                tmpdir,
                "--load",
            ]
            if args.no_cache:
                command.append("--no-cache")
            subprocess.run(
                command,
                check=True,
            )
            Logger.i(f"[Instill Builder] {args.name}:{args.tag} built")
    except subprocess.CalledProcessError:
        Logger.e("[Instill Builder] Build failed")
    except Exception as e:
        Logger.e("[Instill Builder] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")


def push(args):
    try:
        registry = args.url

        subprocess.run(
            [
                "docker",
                "tag",
                f"{args.name}:{args.tag}",
                f"{registry}/{args.name}:{args.tag}",
            ],
            check=True,
        )
        Logger.i("[Instill Builder] Pushing model image...")
        subprocess.run(
            ["docker", "push", f"{registry}/{args.name}:{args.tag}"], check=True
        )
        Logger.i(f"[Instill Builder] {registry}/{args.name}:{args.tag} pushed")
    except subprocess.CalledProcessError:
        Logger.e("[Instill Builder] Push failed")
    except Exception as e:
        Logger.e("[Instill Builder] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")


def run(args):
    try:
        name = uuid.uuid4()

        Logger.i("[Instill Builder] Starting model image...")
        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-d",
                "--name",
                str(name),
                f"{args.name}:{args.tag}",
                "serve",
                "run",
                "_model:entrypoint",
            ],
            check=True,
        )
        time.sleep(10)
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
        Logger.i("[Instill Builder] Model running")
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
        subprocess.run(
            [
                "docker",
                "stop",
                str(name),
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        Logger.e("[Instill Builder] Run failed")
    except Exception as e:
        Logger.e("[Instill Builder] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")


if __name__ == "__main__":
    cli()

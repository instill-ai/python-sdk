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
        "-g",
        "--gpu",
        help="whether the model needs gpu",
        action="store_true",
        required=False,
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
        Logger.i("[Instill] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill] Parsing config file...")
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

            Logger.i("[Instill] Building model image...")
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
            Logger.i(f"[Instill] {args.name}:{args.tag} built")
    except subprocess.CalledProcessError:
        Logger.e("[Instill] Build failed")
    except Exception as e:
        Logger.e("[Instill] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill] Done")


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
        Logger.i("[Instill] Pushing model image...")
        subprocess.run(
            ["docker", "push", f"{registry}/{args.name}:{args.tag}"], check=True
        )
        Logger.i(f"[Instill] {registry}/{args.name}:{args.tag} pushed")
    except subprocess.CalledProcessError:
        Logger.e("[Instill] Push failed")
    except Exception as e:
        Logger.e("[Instill] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill] Done")


def run(args):
    docker_run = False
    try:
        name = uuid.uuid4()
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
                    f"{args.name}:{args.tag}",
                    "serve",
                    "run",
                    "_model:entrypoint",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        else:
            subprocess.run(
                f"docker run --rm -d --shm-size=4gb --name {str(name)} --gpus all {args.name}:{args.tag} /bin/bash -c \
                    \"serve build _model:entrypoint -o serve.yaml && \
                    sed -i 's/app1/default/' serve.yaml && \
                    sed -i 's/num_cpus: 0.0/num_gpus: 1.0/' serve.yaml && \
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
    except Exception as e:
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

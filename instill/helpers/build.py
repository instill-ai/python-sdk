import os
import shutil

import docker
import ray
import yaml

import instill
from instill.helpers.const import DEFAULT_DEPENDENCIES

if __name__ == "__main__":
    client = docker.from_env()
    shutil.copyfile(
        __file__.replace("build.py", "Dockerfile"), os.getcwd() + "/Dockerfile"
    )

    try:
        with open("instill.yaml", "r", encoding="utf8") as f:
            config = yaml.safe_load(f)

        build = config["build"]
        registry = config["registry"]
        repo = config["repo"]
        tag = config["tag"]

        python_version = build["python_version"]
        ray_version = ray.__version__
        instill_version = instill.__version__

        cuda_suffix = "" if not build["gpu"] else "-cu121"

        packages_str = ""
        for p in build["python_packages"]:
            packages_str += p + " "
        for p in DEFAULT_DEPENDENCIES:
            packages_str += p + " "
        packages_str += f"instill-sdk=={instill_version}"

        img, _ = client.images.build(
            path="./",
            rm=True,
            tag=f"{repo}:{tag}",
            buildargs={
                "RAY_VERSION": ray_version,
                "PYTHON_VERSION": python_version,
                "PACKAGES": packages_str,
            },
            quiet=False,
        )
        img.tag(f"{registry}/{repo}", tag)
        client.images.push(f"{registry}/{repo}", tag=tag)
    except Exception as e:
        print(e)
    finally:
        os.remove("Dockerfile")

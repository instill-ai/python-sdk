import os
import shutil
from platform import python_version

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

        ray_version = ray.__version__
        instill_version = instill.__version__

        cuda_suffix = "" if not build["gpu"] else "-cu121"

        pversion = python_version()
        if pversion.split(".")[0] != "3":
            raise RuntimeError("only support python major version = 3")
        if int(pversion.split(".")[1]) < 9 or int(pversion.split(".")[1]) > 11:
            raise RuntimeError("only support python3 minor version >= 9 and <= 11 ")

        pversion = f"3{pversion.split('.')[1]}"

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
                "PYTHON_VERSION": pversion,
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

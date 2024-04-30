import argparse
import subprocess

import yaml

from instill.utils.logger import Logger


def push_image():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        help="image registry url, in the format of host:port, default to docker.io",
        default="docker.io",
        required=False,
    )
    parser.add_argument(
        "-t",
        "--tag",
        help="tag for the model image",
        required=True,
    )

    try:
        args = parser.parse_args()

        Logger.i("[Instill Builder] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill Builder] Parsing config file...")
            config = yaml.safe_load(f)

        registry = args.url
        repo = config["repo"]

        subprocess.run(
            ["docker", "tag", f"{repo}:{args.tag}", f"{registry}/{repo}:{args.tag}"],
            check=True,
        )
        Logger.i("[Instill Builder] Pushing model image...")
        subprocess.run(["docker", "push", f"{registry}/{repo}:{args.tag}"], check=True)
        Logger.i(f"[Instill Builder] {registry}/{repo}:{args.tag} pushed")
    except subprocess.CalledProcessError:
        Logger.e("[Instill Builder] Push failed")
    except Exception as e:
        Logger.e("[Instill Builder] Prepare failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")


if __name__ == "__main__":
    push_image()

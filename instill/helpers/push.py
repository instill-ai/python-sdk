import argparse
import types

import docker
import yaml

from instill.utils.logger import Logger

if __name__ == "__main__":
    Logger.i("[Instill Builder] Setup docker...")
    client = docker.from_env()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        help="image registry url, in the format of host:port, default to docker.io",
        default="docker.io",
        required=False,
    )

    try:
        args = parser.parse_args()

        Logger.i("[Instill Builder] Loading config file...")
        with open("instill.yaml", "r", encoding="utf8") as f:
            Logger.i("[Instill Builder] Parsing config file...")
            config = yaml.safe_load(f)

        registry = args.url
        repo = config["repo"]
        tag = config["tag"]

        img = client.images.get(name=f"{repo}:{tag}")
        img.tag(f"{registry}/{repo}", tag)
        Logger.i("[Instill Builder] Pushing model image...")
        logs = client.images.push(f"{registry}/{repo}", tag=tag)
        if isinstance(logs, types.GeneratorType):
            for line in logs:
                print(*line.values())
        elif isinstance(logs, list):
            for line in logs:
                if "errorDetail" in line:
                    raise RuntimeError(line["errorDetail"]["message"])
                print(line)
        else:
            if "errorDetail" in logs:
                err = logs.split('{"errorDetail":{"message":', 1)[1][1:-4]
                raise RuntimeError(err)
            print(logs)
        Logger.i(f"[Instill Builder] {registry}/{repo}:{tag} pushed")
    except Exception as e:
        Logger.e("[Instill Builder] Push failed")
        Logger.e(e)
    finally:
        Logger.i("[Instill Builder] Done")

"""Push command for the Instill CLI."""

import subprocess

from instill.utils.logger import Logger

from .utils import parse_image_tag_name


def add_push_parser(subcommands):
    """Add push command parser to subcommands."""
    push_parser = subcommands.add_parser("push", help="Push model image")
    push_parser.set_defaults(func=push)
    push_parser.add_argument(
        "name",
        help="""
            Image name and tag for the model with the format <namespace>/<model>[:tag]
            (default tag is 'latest')
        """,
    )
    push_parser.add_argument(
        "-u",
        "--url",
        help="Image registry URL in the format of host:port. If not specified, default to api.instill-ai.com",
        default="api.instill-ai.com",
        required=False,
    )


def push(args):
    """Push a built model image to a Docker registry."""
    registry = args.url
    image_name_tag = parse_image_tag_name(args.name)
    tagged_image = f"{registry}/{image_name_tag}"
    try:
        # Tag the image
        subprocess.run(
            [
                "docker",
                "tag",
                f"{image_name_tag}",
                tagged_image,
            ],
            check=True,
        )
        Logger.i("[Instill] Pushing model image...")
        # Push the image
        subprocess.run(["docker", "push", tagged_image], check=True)
        Logger.i(f"[Instill] {tagged_image} pushed")
    except subprocess.CalledProcessError:
        Logger.e("[Instill] Push failed")
    except (ConnectionError, OSError, IOError) as e:
        Logger.e("[Instill] Prepare failed")
        Logger.e(e)
    finally:
        # Remove the tagged image regardless of success/failure
        try:
            subprocess.run(
                ["docker", "rmi", tagged_image],
                check=True,
            )
        except subprocess.CalledProcessError:
            Logger.e(f"[Instill] Failed to remove tagged image {tagged_image}")
        Logger.i("[Instill] Done")

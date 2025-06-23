import argparse
import platform

from .commands.build import add_build_parser
from .commands.init import add_init_parser
from .commands.push import add_push_parser
from .commands.run import add_run_parser


def cli():
    """Command line interface for the Instill CLI tool."""
    if platform.machine() in ("i386", "AMD64", "x86_64"):
        default_platform = "amd64"
    else:
        default_platform = platform.machine()

    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(required=True)

    # Add command parsers
    add_init_parser(subcommands)
    add_build_parser(subcommands, default_platform)
    add_push_parser(subcommands)
    add_run_parser(subcommands)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    cli()

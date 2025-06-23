"""Initialize command for the Instill CLI."""

import os
import shutil

from instill.utils.logger import Logger


def add_init_parser(subcommands):
    """Add init command parser to subcommands."""
    init_parser = subcommands.add_parser("init", help="Initialize model directory")
    init_parser.set_defaults(func=init)


def init(_):
    """Initialize a new model directory with template files."""
    try:
        shutil.copyfile(
            __file__.replace("commands/init.py", "init-templates/instill.yaml"),
            f"{os.getcwd()}/instill.yaml",
        )
        shutil.copyfile(
            __file__.replace("commands/init.py", "init-templates/model.py"),
            f"{os.getcwd()}/model.py",
        )
        Logger.i("[Instill] Model directory initialized successfully")
    except (OSError, IOError) as e:
        Logger.e("[Instill] Failed to initialize model directory")
        Logger.e(e)

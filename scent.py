"""Configuration file for sniffer."""

import time
import subprocess
import os

from sniffer.api import select_runnable, file_validator, runnable
try:
    from pync import Notifier
except ImportError:
    notify = None
else:
    notify = Notifier.notify


# Watch all relevant directories including subdirectories
watch_paths = [
    "instill",
    "tests",
    "instill/helpers",
    "instill/helpers/commands",
    "instill/clients",
    "instill/resources",
    "instill/utils"
]


class Options:
    group = int(time.time())  # unique per run
    show_coverage = False
    rerun_args = (None, None, None)

    targets = [
        (("make", "test"), "Unit Tests", True),
        (("make", "check"), "Static Analysis", True),
        (("make", "docs", "CI=true"), None, True),
    ]


@select_runnable("run_targets")
@file_validator
def python_files(filename):
    """Check if file is a Python file and should trigger tests."""
    # Ignore cache files and temporary files
    if any(part in filename for part in ["__pycache__", ".pyc", ".pyo", ".pyd", ".py."]):
        return False

    # Only watch Python files in our project directories
    if not filename.endswith(".py"):
        return False

    # Check if file is in one of our watched paths
    for path in watch_paths:
        if filename.startswith(path):
            return True

    return False


@select_runnable("run_targets")
@file_validator
def html_files(filename):
    """Check if file is an HTML/CSS/JS file for docs."""
    return filename.split(".")[-1] in ["html", "css", "js"]


@runnable
def run_targets(*args):
    """Run targets for Python."""
    Options.show_coverage = "coverage" in args

    count = 0
    for count, (command, title, retry) in enumerate(Options.targets, start=1):

        success = call(command, title, retry)
        if not success:
            message = "✅ " * (count - 1) + "❌"
            show_notification(message, title)

            return False

    message = "✅ " * count
    title = "All Targets"
    show_notification(message, title)
    show_coverage()

    return True


def call(command, title, retry):
    """Run a command-line program and display the result."""
    if Options.rerun_args[0] is not None:
        command, title, retry = Options.rerun_args
        Options.rerun_args = (None, None, None)
        success = call(command, title, retry)
        if not success:
            return False

    print("")
    print(f"$ {' '.join(command)}")
    failure = subprocess.call(command)

    if failure and retry:
        Options.rerun_args = command, title, retry

    return not failure


def show_notification(message, title):
    """Show a user notification."""
    if notify and title:
        notify(message, title=title, group=Options.group)


def show_coverage():
    """Launch the coverage report."""
    if Options.show_coverage:
        subprocess.call(["make", "read-coverage"])

    Options.show_coverage = False

import os

IGNORE_FILES = {
    ".bash_logout",
    ".bashrc",
    ".profile",
    ".sudo_as_admin_successful",
    "pip-freeze.txt",
    "requirements_compiled.txt",
}

IGNORE_FOLDERS = {
    ".cache",
    ".conda",
    ".whl",
    "anaconda3",
}


def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                if entry.name in IGNORE_FILES:
                    continue
                total += entry.stat().st_size
            elif entry.is_dir():
                if entry.name in IGNORE_FOLDERS:
                    continue
                total += get_dir_size(entry.path)
    return total

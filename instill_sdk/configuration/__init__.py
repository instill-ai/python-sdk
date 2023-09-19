import os
import typing as t
from pathlib import Path

import yaml
from pydantic import BaseModel

CONFIG_DIR = Path(
    os.getenv(
        "INSTILL_SYSTEM_CONFIG_PATH",
        Path.home() / ".config/instill/",
    )
)


class _InstillHost(BaseModel):
    alias: t.Optional[str] = ""
    url: str
    token: t.Optional[str] = ""


class _Config(BaseModel):
    remotes: t.Optional[t.List[_InstillHost]] = None


class Configuration:
    def __init__(self) -> None:
        self._config: _Config

        CONFIG_DIR.mkdir(exist_ok=True)

    @property
    def remotes(self) -> t.Optional[t.List[_InstillHost]]:
        return self._config.remotes

    def load(self) -> None:
        path = CONFIG_DIR / "config.yaml"
        if not path.exists():
            self._config = _Config()
            return
        try:
            with open(path, "r", encoding="utf-8") as c:
                self._config = _Config.model_validate(
                    yaml.load(c, Loader=yaml.FullLoader)
                )
        except Exception as e:
            raise BaseException(f"Invalid configuration file at '{path}'") from e


config = Configuration()
config.load()

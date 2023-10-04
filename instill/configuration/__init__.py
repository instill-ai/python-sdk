import json
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
    url: str
    secure: bool
    token: str


class _Config(BaseModel):
    hosts: t.Dict[str, _InstillHost] = {}


class Configuration:
    def __init__(self) -> None:
        self._config: _Config

        CONFIG_DIR.mkdir(exist_ok=True)

    @property
    def hosts(self) -> t.Dict[str, _InstillHost]:
        return self._config.hosts

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

    def save(self) -> None:
        path = CONFIG_DIR / "config.yaml"

        CONFIG_DIR.mkdir(exist_ok=True)

        with open(path, "w", encoding="utf-8") as c:
            yaml.dump(
                json.loads(
                    self._config.model_dump_json(
                        exclude_none=True,
                    )
                ),
                c,
            )

    def set_token(self, alias: str, token: str) -> None:
        if self._config.hosts is not None:
            self._config.hosts[alias].token = token
            self.save()


global_config = Configuration()
global_config.load()

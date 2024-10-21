# pylint: disable=no-name-in-module
import json
import os
import typing as t
from pathlib import Path

import yaml
from pydantic import BaseModel

from instill.helpers.const import HOST_URL_PROD

CONFIG_DIR = Path(
    os.getenv(
        "INSTILL_SYSTEM_CONFIG_PATH",
        Path.home() / ".config/instill/sdk/python/",
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
        self.load()

        if "default" not in self._config.hosts:
            self.set_default(url=HOST_URL_PROD, secure=True, token="")

        CONFIG_DIR.mkdir(exist_ok=True)

    @property
    def hosts(self) -> t.Dict[str, _InstillHost]:
        return self._config.hosts

    def load(self) -> None:
        path = CONFIG_DIR / "config.yml"
        if not path.exists():
            self._config = _Config()
            return
        try:
            with open(path, "r", encoding="utf-8") as c:
                self._config = _Config.validate(yaml.load(c, Loader=yaml.FullLoader))
        except Exception as e:
            raise BaseException(f"Invalid configuration file at '{path}'") from e

    def save(self) -> None:
        path = CONFIG_DIR / "config.yml"

        CONFIG_DIR.mkdir(exist_ok=True)

        with open(path, "w", encoding="utf-8") as c:
            yaml.dump(
                json.loads(
                    self._config.json(
                        exclude_none=True,
                    )
                ),
                c,
            )

    def set_default(self, url: str, token: str, secure: bool):
        self._config.hosts["default"] = _InstillHost(
            url=url, secure=secure, token=token
        )


global_config = Configuration()

class ModelPathException(Exception):
    def __str__(self) -> str:
        return "model path is not valid"


class ModelVramException(Exception):
    def __str__(self) -> str:
        return "model projected vram usage is more than the GPU can handle"


class ModelConfigException(Exception):
    def __init__(self, field):
        self.field = field

    def __str__(
        self,
    ) -> str:
        return f"model config file `instill.yaml` is missing {self.field} field"

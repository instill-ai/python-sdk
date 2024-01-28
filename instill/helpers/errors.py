class ModelPathException(Exception):
    def __str__(self) -> str:
        return "model path is not valid"


class ModelVramException(Exception):
    def __str__(self) -> str:
        return "model projected vram usage is more than the GPU can handle"

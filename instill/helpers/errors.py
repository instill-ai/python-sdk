"""
Exceptions for the Instill CLI tool.
"""


class ModelPathException(Exception):
    """
    Exception raised when the model path is not valid.
    """

    def __str__(self) -> str:
        return "model path is not valid"


class ModelVramException(Exception):
    """
    Exception raised when the model projected vram usage is more than the GPU can handle.
    """

    def __str__(self) -> str:
        return "model projected vram usage is more than the GPU can handle"


class ModelConfigException(Exception):
    """
    Exception raised when the model config file `instill.yaml` is missing a required field.
    """

    def __init__(self, field):
        self.field = field

    def __str__(
        self,
    ) -> str:
        return f"model config file `instill.yaml` is missing {self.field} field"


class InvalidInputException(Exception):
    """
    Exception raised when the input is invalid.
    """

    def __init__(self, field):
        self.field = field

    def __str__(
        self,
    ) -> str:
        return f"trigger request input error: {self.field}"


class InvalidOutputShapeException(Exception):
    """
    Exception raised when the output shape is invalid.
    """

    def __str__(self) -> str:
        return "outputs length not matched"

class ModelPathException(Exception):
    def __str__(self) -> str:
        return "model path is not valid"

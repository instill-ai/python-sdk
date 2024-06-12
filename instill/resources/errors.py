class WrongModeException(Exception):
    def __str__(self) -> str:
        return "Instill Model Connector mode error"

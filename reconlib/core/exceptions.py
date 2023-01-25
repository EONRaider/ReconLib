class ReconLibException(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class InvalidTargetError(ReconLibException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(f"{self.__class__.__name__}: {message}", code)

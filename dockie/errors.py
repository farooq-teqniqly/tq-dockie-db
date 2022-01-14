from abc import ABC


class DockieError(ABC, Exception):
    def __init__(self, message: str, error_number: int):
        self.error_number = error_number
        super().__init__(message)


class ObjectCreateError(DockieError):
    def __init__(self, message):
        super().__init__(message, 1000)


class ObjectReadError(DockieError):
    def __init__(self, message):
        super().__init__(message, 1001)

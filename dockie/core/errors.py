"""
Errors module.
"""
from abc import ABC


class DockieError(ABC, Exception):
    """
    Represents an error raised by the document database. The DockieError class
    is the base class of all errors.
    """

    def __init__(self, message: str, error_number: int):
        self.error_number = error_number
        super().__init__(message)


class ObjectCreateError(DockieError):
    """
    Represents an error that occurs during a create operation.
    """

    def __init__(self, message):
        super().__init__(message, 1000)


class ObjectReadError(DockieError):
    """
    Represents an error that occurs during a read operation.
    """

    def __init__(self, message):
        super().__init__(message, 1001)


class ObjectNotFoundError(DockieError):
    """
    Represents an error that occurs when an object is not found.
    """

    def __init__(self, message):
        super().__init__(message, 1002)


class QueryError(DockieError):
    """
    Represents an error that occurs during a query operation.
    """

    def __init__(self, message):
        super().__init__(message, 1003)


class IdTypeNotSupportedError(DockieError):
    """
    Represents an error that occurs on an attempt to create a document with
    an unsupported id type.
    """

    def __init__(self, message):
        super().__init__(message, 1004)


class PersistenceError(DockieError):
    """
    Represents an error that occurs during a database persistence operation.
    """

    def __init__(self, message):
        super().__init__(message, 1005)

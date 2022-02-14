"""
Ensure module. An 'Ensure' is used to validate pre-conditions and post-conditions.
"""
from dockie.core import errors


def _is_none_or_whitespace(value: str) -> bool:
    return value is None or len(value.strip()) == 0


def _is_none(obj) -> bool:
    return obj is None


def not_none_or_whitespace(value: str, error_to_raise: errors.DockieError):
    """
    Ensures the string is not None or whitespace.
    :param value: The string to verify.
    :param error_to_raise: The error raised when the condition is not met.
    """
    if _is_none_or_whitespace(value):
        raise error_to_raise


def not_none(obj, error_to_raise: errors.DockieError):
    """
    Ensures the object is not None.
    :param obj: The object to verify.
    :param error_to_raise: The error raised when the condition is not met.
    """
    if _is_none(obj):
        raise error_to_raise


def id_specified(document_id, error_to_raise: errors.DockieError):
    """
    Ensures a Document has a document id of a supported type.
    :param document_id: The document id to verify.
    :param error_to_raise: The error raised when the condition is not met.
    """
    if type(document_id) not in [str, int]:
        raise errors.IdTypeNotSupportedError(
            "Supported document_id types are 'int' and 'str'."
        )

    if isinstance(document_id, str):
        if _is_none_or_whitespace(document_id):
            raise error_to_raise

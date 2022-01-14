import dockie.core.errors as errors


def _is_none_or_whitespace(s: str) -> bool:
    return s is None or len(s.strip()) == 0


def _is_none(obj) -> bool:
    return obj is None


def not_none_or_whitespace(s: str, error_to_raise: errors.DockieError):
    if _is_none_or_whitespace(s):
        raise error_to_raise


def not_none(obj, error_to_raise: errors.DockieError):
    if _is_none(obj):
        raise error_to_raise


def id_specified(document_id, error_to_raise: errors.DockieError):
    if type(document_id) not in [str, int]:
        raise errors.IdTypeNotSupportedError(
            "Supported document_id types are 'int' and 'str'."
        )

    if type(document_id) == str:
        if _is_none_or_whitespace(document_id):
            raise error_to_raise

    if _is_none(document_id):
        raise error_to_raise

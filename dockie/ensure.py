import dockie.errors as errors


def not_none_or_whitespace(s: str, error_to_raise: errors.DockieError):
    if s is None or len(s.strip()) == 0:
        raise error_to_raise


def not_none(obj, error_to_raise: errors.DockieError):
    if obj is None:
        raise error_to_raise

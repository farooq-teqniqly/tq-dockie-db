import dockie.core.errors as errors


def test_object_create_error():
    _assert_error(errors.ObjectCreateError("foo"), "foo", 1000)


def test_object_read_error():
    _assert_error(errors.ObjectReadError("foo"), "foo", 1001)


def test_object_not_found_error():
    _assert_error(errors.ObjectNotFoundError("foo"), "foo", 1002)


def test_query_error():
    _assert_error(errors.QueryError("foo"), "foo", 1003)


def _assert_error(
    error: errors.DockieError, expected_message: str, expected_error_number: int
):
    assert error.args[0] == expected_message
    assert error.error_number == expected_error_number

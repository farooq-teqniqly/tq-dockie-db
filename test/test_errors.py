import dockie.errors as errors


def test_object_create_error():
    message = "foo"
    error = errors.ObjectCreateError(message)
    assert error.args[0] == message
    assert error.error_number == 1000


def test_object_read_error():
    message = "foo"
    error = errors.ObjectReadError(message)
    assert error.args[0] == message
    assert error.error_number == 1001

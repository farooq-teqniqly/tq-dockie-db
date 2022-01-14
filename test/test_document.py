import pytest

from dockie.core.document import Document
import dockie.core.errors as errors


def test_raise_error_when_document_id_not_specified():
    with pytest.raises(errors.ObjectCreateError):
        Document(document_id=None, data={})
        Document(document_id="", data={})


def test_raise_error_when_document_data_is_none():
    with pytest.raises(errors.ObjectCreateError):
        Document(1, None)


def test_can_get_document_data():
    data = {"foo": "bar"}
    doc = Document("doc1", data)
    assert doc.get_data() == data


def test_can_create_document_with_int_id():
    data = {"foo": "bar"}
    doc = Document(1, data)
    assert doc.get_id() == 1


def test_raise_error_when_creating_document_with_unsupported_id_type():
    with pytest.raises(errors.ObjectCreateError):
        Document(True, {"foo": "bar"})

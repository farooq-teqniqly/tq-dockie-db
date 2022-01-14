import pytest

from dockie.document import Document
import dockie.errors as errors


def test_raise_error_when_document_id_not_specified():
    with pytest.raises(errors.ObjectCreateError):
        Document(document_id=None, data={})
        Document(document_id="", data={})


def test_can_get_document_data():
    data = {"foo": "bar"}
    doc = Document("doc1", data)
    assert doc.get_data() == data

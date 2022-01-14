import pytest

from dockie.core import errors
from dockie.core.container import Container
from dockie.core.document import Document
from dockie.query.query import DocumentAttributeQuery


def test_can_query_documents_by_attribute_simple():
    container = Container("shop")
    documents = [
        {"id": "doc1", "name": "Farooq"},
        {"id": "doc2", "name": "Farooq"},
        {"id": "doc3", "name": "Noor"},
    ]

    for document in documents:
        container.add_document(Document(document["id"], document))

    query = DocumentAttributeQuery()
    actual_documents = query.execute(container, query='name=="Farooq"')

    assert len(actual_documents) == 2


def test_can_query_documents_by_attribute_complex():
    container = Container("shop")

    documents = [
        {"id": "doc1", "bio": {"name": "Farooq"}},
        {"id": "doc2", "bio": {"name": "Noor"}},
        {"id": "doc3", "bio": {"name": "Yasin"}},
    ]

    for document in documents:
        container.add_document(Document(document["id"], document))

    query = DocumentAttributeQuery()
    actual_documents = query.execute(container, query='`bio.name`=="Farooq"')

    assert len(actual_documents) == 1


def test_query_returns_empty_list_when_no_documents_found():
    container = Container("shop")

    documents = [{"id": "doc1", "bio": {"name": "Farooq"}}]

    for document in documents:
        container.add_document(Document(document["id"], document))

    query = DocumentAttributeQuery()
    actual_documents = query.execute(container, query='`bio.name`!="Farooq"')

    assert len(actual_documents) == 0


def test_query_raises_error_when_query_not_specified():
    container = Container("shop")
    query = DocumentAttributeQuery()

    with pytest.raises(errors.QueryError):
        query.execute(container)

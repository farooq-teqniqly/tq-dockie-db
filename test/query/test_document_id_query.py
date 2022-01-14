from dockie.core.container import Container
from dockie.core.document import Document
from dockie.query.query import DocumentIdQuery


def test_can_query_document_by_id():
    container = Container("shop")
    expected_document = Document(100, {"foo": "bar"})
    container.add_document(expected_document)

    query = DocumentIdQuery()
    actual_document = query.execute(container, document_id=100)

    assert actual_document.get_id() == 100

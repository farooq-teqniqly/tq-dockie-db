from typing import Optional

import pytest

from dockie.core.document import Document
from dockie.core.container import Container
import dockie.core.errors as errors

container: Optional[Container] = None


def setup_module(module):
    global container
    container = Container("shop")


def test_new_container_has_no_documents():
    assert len(container.list_documents()) == 0


def test_can_add_documents():
    item_document = Document(
        "item1", {"name": "basketball", "description": "A basketball"}
    )

    order_document = Document("order1", {"id": "order1", "items": ["item1"]})
    container.add_document(item_document)
    container.add_document(order_document)

    assert "item1" in container.list_documents()
    assert "order1" in container.list_documents()


def test_raise_error_when_container_name_not_specified():
    with pytest.raises(errors.ObjectCreateError):
        Container("")
        Container(None)

from typing import Optional

import pytest

from dockie.database import Database
from dockie.document import Document
import dockie.errors as errors

db: Optional[Database] = None


def setup_module(module):
    global db
    db = Database("test")


def test_new_container_has_no_documents():
    db.add_container("shop")
    assert db.get_container("shop") is not None
    assert len(db.get_container("shop").list_documents()) == 0


def test_can_add_documents():
    item_document = Document(
        "item1", {"name": "basketball", "description": "A basketball"}
    )

    order_document = Document("order1", {"id": "order1", "items": ["item1"]})
    shop_container = db.get_container("shop")

    shop_container.add_document(item_document)
    shop_container.add_document(order_document)

    assert "item1" in shop_container.list_documents()
    assert "order1" in shop_container.list_documents()


def test_raise_error_when_container_name_not_specified():
    with pytest.raises(errors.ObjectCreateError):
        db.add_container("")
        db.add_container(None)

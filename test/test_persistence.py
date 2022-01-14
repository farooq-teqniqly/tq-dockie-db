import os
from typing import Optional

import pytest

from dockie.core import errors
from dockie.core.database import Database
from dockie.core.document import Document
from dockie.core.persistence import persist_to_file, load_from_file

db: Optional[Database] = None
filename = os.path.join(os.getcwd(), "db.bak")


def setup_module(module):
    global db
    db = Database()
    db.add_container("orders")

    orders_container = db.get_container("orders")
    orders_container.add_document(Document("order1", {"customerId": 100}))


def test_persist_database():
    if os.path.exists(filename):
        os.remove(filename)

    try:
        persist_to_file(db, filename)
        assert os.path.exists(filename)

        db_from_file = load_from_file(filename)

        assert (
            db_from_file.get_container("orders")
            .get_document("order1")
            .get_data()["customerId"]
            == 100
        )
    finally:
        os.remove(filename)


def test_raise_error_when_file_exists():
    if os.path.exists(filename):
        os.remove(filename)

    persist_to_file(db, filename)

    try:
        with pytest.raises(errors.PersistenceError):
            persist_to_file(db, filename)
    finally:
        os.remove(filename)


def test_overwrite_file():
    if os.path.exists(filename):
        os.remove(filename)

    try:
        persist_to_file(db, filename)
        assert os.path.exists(filename)
        persist_to_file(db, filename, overwrite=True)
        assert os.path.exists(filename)
    finally:
        os.remove(filename)


def test_load_from_file_raises_error_when_file_not_found():
    with pytest.raises(errors.PersistenceError):
        load_from_file("foo.bak")

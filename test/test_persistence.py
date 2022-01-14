import os

from dockie.core.database import Database
from dockie.core.document import Document
from dockie.core.persistence import persist_to_file, load_from_file


def test_persist_database():
    db = Database("db")
    db.add_container("orders")

    orders_container = db.get_container("orders")
    orders_container.add_document(Document("order1", {"customerId": 100}))

    filename = os.path.join(os.getcwd(), "db.bak")

    if os.path.exists(filename):
        os.remove(filename)

    try:
        persist_to_file(db, filename)
        assert os.path.exists(filename)

        db_from_file = load_from_file(filename)
        assert db_from_file.get_name() == "db"

        assert (
            db_from_file.get_container("orders")
            .get_document("order1")
            .get_data()["customerId"]
            == 100
        )
    finally:
        os.remove(filename)

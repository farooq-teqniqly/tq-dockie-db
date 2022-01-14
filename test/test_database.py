from typing import Optional

import pytest

from dockie.database import Database

db: Optional[Database] = None


def setup_module(module):
    global db
    db = Database("shop")


def test_can_create_database():
    assert db.get_name() == "shop"


def test_new_database_has_no_containers():
    assert len(db.list_containers()) == 0


def test_raise_error_when_database_name_not_specified():
    with pytest.raises(ValueError):
        Database("")
        Database(None)


def test_add_container_raises_error_when_container_exists():
    db.add_container("shop")

    with pytest.raises(ValueError):
        db.add_container("shop")


def test_add_container_raises_error_when_container_name_not_specified():
    with pytest.raises(ValueError):
        db.add_container("")
        db.add_container(None)

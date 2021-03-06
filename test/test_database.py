from typing import Optional

import pytest

from dockie.core.database import Database
import dockie.core.errors as errors

db: Optional[Database] = None


def setup_module(module):
    global db
    db = Database()


def test_new_database_has_no_containers():
    assert len(db.list_containers()) == 0


def test_add_container_raises_error_when_container_exists():
    db.add_container("shop")

    with pytest.raises(errors.ObjectCreateError) as e:
        db.add_container("shop")


def test_add_container_raises_error_when_container_name_not_specified():
    invalid_names = ["", None]

    for invalid_name in invalid_names:
        with pytest.raises(errors.ObjectCreateError) as e:
            db.add_container(invalid_name)


def test_container_raises_error_when_container_not_found():
    with pytest.raises(errors.ObjectNotFoundError):
        db.get_container("foobar")

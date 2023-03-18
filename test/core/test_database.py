import pytest
import os

from dockie.core.database import Database


@pytest.fixture
def db(tmp_path):
    db_root = tmp_path / 'my_databases'
    db_name = 'test_database'
    return Database(db_root, db_name)


def test_insert(db):
    doc = {'id': '1', 'title': 'First Document', 'content': 'Hello, world!'}
    doc_id = db.insert(doc)
    assert doc_id == '1'
    assert os.path.exists(db.document_manager._get_file_path(doc_id))


def test_get(db):
    doc = {'id': '2', 'title': 'Second Document', 'content': 'Hello, world again!'}
    db.insert(doc)
    retrieved_doc = db.get('2')
    assert retrieved_doc == doc


def test_update(db):
    doc = {'id': '3', 'title': 'Third Document', 'content': 'To be updated'}
    db.insert(doc)

    updated_doc = {'id': '3', 'title': 'Updated Document', 'content': 'This is an updated document.'}
    db.update('3', updated_doc)
    retrieved_doc = db.get('3')
    assert retrieved_doc == updated_doc


def test_delete(db):
    doc = {'id': '4', 'title': 'Fourth Document', 'content': 'To be deleted'}
    db.insert(doc)
    file_path = db.document_manager._get_file_path('4')
    assert os.path.exists(file_path)

    db.delete('4')
    assert not os.path.exists(file_path)
    with pytest.raises(KeyError):
        db.get('4')


def test_key_error_on_duplicate_insert(db):
    doc = {'id': '5', 'title': 'Duplicate Document', 'content': 'Duplicate insert test'}
    db.insert(doc)
    with pytest.raises(KeyError):
        db.insert(doc)


def test_key_error_on_nonexistent_get(db):
    with pytest.raises(KeyError):
        db.get('nonexistent')


def test_key_error_on_nonexistent_update(db):
    doc = {'id': 'nonexistent', 'title': 'Nonexistent Document', 'content': 'Nonexistent update test'}
    with pytest.raises(KeyError):
        db.update('nonexistent', doc)


def test_key_error_on_nonexistent_delete(db):
    with pytest.raises(KeyError):
        db.delete('nonexistent')


def test_value_error_on_id_change(db):
    doc = {'id': '6', 'title': 'ID Change Document', 'content': 'ID change test'}
    db.insert(doc)

    updated_doc = {'id': '7', 'title': 'ID Change Document', 'content': 'ID change test'}
    with pytest.raises(ValueError):
        db.update('6', updated_doc)


def test_index_loaded(db, tmp_path):
    # Insert a document
    doc = {'id': 'index_loaded', 'title': 'Index Loaded Test', 'content': 'Testing index loading'}
    db.insert(doc)

    # Create a new instance of the Database with the same database name
    db_root = tmp_path / 'my_databases'
    db_name = 'test_database'
    new_db = Database(db_root, db_name)

    # Check if the document can be retrieved from the new instance
    retrieved_doc = new_db.get('index_loaded')
    assert retrieved_doc == doc

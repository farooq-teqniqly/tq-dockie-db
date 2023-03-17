import html
import os
import shutil
import pytest
from dockie.api.server import app
import dockie.core.database_defaults as defaults

TEST_DB_ROOT = 'test_databases'
TEST_DB_NAME = 'test_db'


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True

    # Set up test environment
    os.makedirs(TEST_DB_ROOT, exist_ok=True)

    with app.test_client() as client:
        yield client

    # Tear down test environment
    shutil.rmtree(TEST_DB_ROOT)


def test_init_db(client):
    response = client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    assert response.status_code == 201
    assert response.get_json() == {'message': "Database 'test_db' initialized"}


def test_insert_document(client):
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    doc = {'id': '1', 'title': 'Test Document', 'content': 'This is a test document'}
    response = client.post('/test_db/insert', json=doc)
    assert response.status_code == 201
    assert response.get_json() == {'id': '1'}


def test_get_document(client):
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    doc = {'id': '1', 'title': 'Test Document', 'content': 'This is a test document'}
    client.post('/test_db/insert', json=doc)
    response = client.get('/test_db/get/1')
    assert response.status_code == 200
    assert response.get_json() == doc


def test_delete_document(client):
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    doc = {'id': '1', 'title': 'Test Document', 'content': 'This is a test document'}
    client.post('/test_db/insert', json=doc)
    response = client.delete('/test_db/delete/1')
    assert response.status_code == 200
    assert response.get_json() == {'message': "Document '1' deleted"}


def test_update_document(client):
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    doc = {'id': '1', 'title': 'Test Document', 'content': 'This is a test document'}
    client.post('/test_db/insert', json=doc)
    updated_doc = {'id': '1', 'title': 'Updated Test Document', 'content': 'This is an updated test document'}
    response = client.put('/test_db/update/1', json=updated_doc)
    assert response.status_code == 200
    assert response.get_json() == {'message': "Document '1' updated"}


def test_init_db_no_name(client):
    response = client.post('/init', json={'db_root': TEST_DB_ROOT})
    assert response.status_code == 400
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert "Database name is required" in decoded_response


def test_insert_document_nonexistent_db(client):
    non_existent_db_name = 'non_existent_db'
    doc = {'id': '1', 'title': 'Test Document', 'content': 'This is a test document'}
    response = client.post(f'/{non_existent_db_name}/insert', json=doc)
    assert response.status_code == 404
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Database '{non_existent_db_name}' not found" in decoded_response


def test_get_document_nonexistent_db(client):
    non_existent_db_name = "non_existent_db"
    response = client.get(f'/{non_existent_db_name}/get/1')
    assert response.status_code == 404
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Database '{non_existent_db_name}' not found" in decoded_response


def test_get_document_nonexistent_document(client):
    non_existent_document_id = 10000
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    response = client.get(f'/test_db/get/{non_existent_document_id}')
    assert response.status_code == 404
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Document with ID '{non_existent_document_id}' not found." in decoded_response

def test_delete_document_nonexistent_db(client):
    non_existent_db_name = "non_existent_db"
    response = client.delete(f'/{non_existent_db_name}/delete/1')
    assert response.status_code == 404
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Database '{non_existent_db_name}' not found" in decoded_response

def test_delete_document_nonexistent_document(client):
    non_existent_document_id = 10000
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    response = client.delete(f'/test_db/delete/{non_existent_document_id}')
    assert response.status_code == 404
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Document with ID '{non_existent_document_id}' not found." in decoded_response

def test_update_document_nonexistent_db(client):
    non_existent_db_name = "non_existent_db"
    updated_doc = {'id': '1', 'title': 'Updated Test Document', 'content': 'This is an updated test document'}
    response = client.put(f'/{non_existent_db_name}/update/1', json=updated_doc)
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Database '{non_existent_db_name}' not found" in decoded_response

def test_update_document_nonexistent_document(client):
    non_existent_document_id = 10000
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    updated_doc = {'id': non_existent_document_id, 'title': 'Updated Test Document', 'content': 'This is an updated test document'}
    response = client.put(f'/test_db/update/{non_existent_document_id}', json=updated_doc)
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"Document with ID '{non_existent_document_id}' not found." in decoded_response

def test_update_document_document_id_changed(client):
    client.post('/init', json={'db_root': TEST_DB_ROOT, 'db_name': 'test_db'})
    doc = {'id': '1', 'title': 'Test Document', 'content': 'This is a test document'}
    client.post('/test_db/insert', json=doc)
    updated_doc = {'id': '2', 'title': 'Updated Test Document', 'content': 'This is an updated test document'}
    response = client.put(f'/test_db/update/1', json=updated_doc)
    decoded_response = html.unescape(response.data.decode(defaults.ENCODING))
    assert f"The document's ID cannot be changed." in decoded_response

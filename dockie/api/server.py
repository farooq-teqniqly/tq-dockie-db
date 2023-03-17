"""This module provides an API for DockieDB.

This module uses Flask framework to handle HTTP requests for managing databases and documents.
It provides endpoints for creating and initializing a new database, inserting, retrieving,
updating and deleting documents within a specific database.

This module depends on the dockie.core.database module, which provides a Database class for
managing documents in a database.

Example:
    To create a new database:
        POST /init
        body: {
            "db_name": "my_database",
            "db_root": "/path/to/root/folder/for/my_database"
        }

    To insert a new document into the 'my_database':
        POST /my_database/insert
        body: {
            "name": "Farooq",
            "age": 45
        }

    To retrieve a document with id '123' from 'my_database':
        GET /my_database/get/123

    To update an existing document with id '123' in 'my_database':
        PUT /my_database/update/123
        body: {
            "name": "Morgan",
            "age": 42
        }

    To delete an existing document with id '123' from 'my_database':
        DELETE /my_database/delete/123
"""
from flask import Flask, request, jsonify, abort
from dockie.core.database import Database

app = Flask(__name__)
databases = {}


@app.route('/init', methods=['POST'])
def init_db():
    """
        Initialize a new database.

        This function creates a new database with the provided name and root directory,
        and adds it to the list of databases.

        Returns:
            response (str): A JSON response indicating whether the database
            was successfully created or not.

        Raises:
            400 Bad Request: If the request does not contain a valid database name.
            400 Bad Request: If a database with the same name already exists.
    """
    data = request.get_json()
    db_root = data.get('db_root', 'my_databases')
    db_name = data.get('db_name')

    if not db_name:
        abort(400, "Database name is required")

    if db_name in databases:
        abort(400, f"Database '{db_name}' already exists")

    databases[db_name] = Database(db_root, db_name)
    return jsonify({'message': f"Database '{db_name}' initialized"}), 201


@app.route('/<db_name>/insert', methods=['POST'])
def insert_document(db_name):
    """
       Insert a new document into a database.

       This function inserts a new document into the specified database.

       Args:
           db_name (str): The name of the database to insert the document into.

       Returns:
           response (str): A JSON response containing the ID of the inserted document.

       Raises:
           404 Not Found: If the specified database does not exist.
           400 Bad Request: If the request does not contain a valid document.
   """
    if db_name not in databases:
        abort(404, f"Database '{db_name}' not found")

    document = request.get_json()
    try:
        doc_id = databases[db_name].insert(document)
        return jsonify({'id': doc_id}), 201
    except KeyError as key_error:
        return str(key_error), 400


@app.route('/<db_name>/get/<doc_id>', methods=['GET'])
def get_document(db_name, doc_id):
    """
        Retrieve a document from a database.

        This function retrieves a document with the specified ID from the specified database.

        Args:
            db_name (str): The name of the database to retrieve the document from.
            doc_id (str): The ID of the document to retrieve.

        Returns:
            response (str): A JSON response containing the retrieved document.

        Raises:
            404 Not Found: If the specified database or document does not exist.
    """
    if db_name not in databases:
        abort(404, f"Database '{db_name}' not found")

    try:
        document = databases[db_name].get(doc_id)
        return jsonify(document)
    except KeyError as key_error:
        return str(key_error), 404


@app.route('/<db_name>/delete/<doc_id>', methods=['DELETE'])
def delete_document(db_name, doc_id):
    """
        Delete a document from a database.

        This function deletes a document with the specified ID from the specified database.

        Args:
            db_name (str): The name of the database to delete the document from.
            doc_id (str): The ID of the document to delete.

        Returns:
            response (str): A JSON response indicating whether the document
            was successfully deleted or not.

        Raises:
            404 Not Found: If the specified database or document does not exist.
    """
    if db_name not in databases:
        abort(404, f"Database '{db_name}' not found")

    try:
        databases[db_name].delete(doc_id)
        return jsonify({'message': f"Document '{doc_id}' deleted"})
    except KeyError as key_error:
        return str(key_error), 404


@app.route('/<db_name>/update/<doc_id>', methods=['PUT'])
def update_document(db_name, doc_id):
    """
        Update a document in the specified database with the given ID.

        Args:
            db_name (str): The name of the database to update the document in.
            doc_id (str): The ID of the document to update.

        Returns:
            response (str): A JSON response indicating whether the document
            was successfully updated or not.

        Raises:
            404 Not Found: If the specified database or document does not exist.
            400 Bad Request: If the request does not contain a valid updated document.
    """
    if db_name not in databases:
        abort(404, f"Database '{db_name}' not found")

    updated_document = request.get_json()
    try:
        databases[db_name].update(doc_id, updated_document)
        return jsonify({'message': f"Document '{doc_id}' updated"})
    except KeyError as key_error:
        return str(key_error), 404
    except ValueError as value_error:
        return str(value_error), 400


if __name__ == '__main__':
    app.run()

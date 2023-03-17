"""The DockieDb database module.

This module provides a simple document database implementation for managing JSON
documents using a file-based storage system. It supports basic CRUD operations
(create, read, update, and delete) on documents, which are stored in separate files
within a specified database directory.
"""

import json
import os
import dockie.core.database_defaults as defaults


class Database:
    """A document database class for managing and persisting JSON documents.

        This class provides a document database implementation for managing JSON
        documents using a file-based storage system. It supports basic CRUD operations
        (create, read, update, and delete) on documents, which are stored in separate files
        within a specified database directory.

        Attributes:
            db_directory (str): The path to the database directory.
            index_file (str): The path to the index file, which maps document IDs to file paths.
            index (dict): A dictionary that maps document IDs to file paths.
    """

    def __init__(self, db_root, db_name):
        """Initializes a new instance of the Database class. The database's location will be
        in the folder /[db_root]/[db_name]

                Args:
                    db_root (str): The path to the root directory containing all databases.
                    db_name (str): The name of the database.
        """
        self.db_directory = os.path.join(db_root, db_name)

        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)

        self.index_file = os.path.join(self.db_directory, f'{db_name}.json')
        self.index = self._load_index()

    def _load_index(self):
        """Loads the index from the index file, or creates an empty index if the file doesn't exist.

                Returns:
                    dict: The index dictionary.
        """
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r', encoding=defaults.ENCODING) as file:
                index = json.load(file)
        else:
            index = {}
        return index

    def _save_index(self):
        """Saves the index to the index file."""
        with open(self.index_file, 'w', encoding=defaults.ENCODING) as file:
            json.dump(self.index, file)

    def _get_file_path(self, doc_id):
        """Generates the file path for a document with the given ID.

                Args:
                    doc_id (str): The ID of the document.

                Returns:
                    str: The file path for the document.
        """
        return os.path.join(self.db_directory, f'{doc_id}.json')

    def insert(self, document):
        """Inserts a new document into the database.

                Args:
                    document (dict): The document to insert.

                Returns:
                    str: The ID of the inserted document.

                Raises:
                    KeyError: If a document with the same ID already exists.
        """
        doc_id = document['id']

        if doc_id in self.index:
            raise KeyError(f"Document with ID '{doc_id}' already exists.")
        file_path = self._get_file_path(doc_id)

        with open(file_path, 'w', encoding=defaults.ENCODING) as file:
            json.dump(document, file)

        self.index[doc_id] = file_path
        self._save_index()

        return doc_id

    def get(self, doc_id):
        """Retrieves a document with the specified ID from the database.

                Args:
                    doc_id (str): The ID of the document to retrieve.

                Returns:
                    dict: The retrieved document.

                Raises:
                    KeyError: If a document with the specified ID does not exist.
        """
        if doc_id not in self.index:
            raise KeyError(f"Document with ID '{doc_id}' not found.")

        file_path = self.index[doc_id]

        with open(file_path, 'r', encoding=defaults.ENCODING) as file:
            document = json.load(file)

        return document

    def delete(self, doc_id):
        """Delete a document from the database by its ID.

                Args:
                    doc_id (str): The unique ID of the document.

                Raises:
                    KeyError: If the document with the given ID is not found.
        """
        if doc_id not in self.index:
            raise KeyError(f"Document with ID '{doc_id}' not found.")

        file_path = self.index[doc_id]
        os.remove(file_path)
        del self.index[doc_id]
        self._save_index()

    def update(self, doc_id, updated_document):
        """Update a document in the database.

                Args:
                    doc_id (str): The unique ID of the document to update.
                    updated_document (dict): The updated document.

                Raises:
                    KeyError: If the document with the given ID is not found.
                    ValueError: If the document's ID is changed.
        """
        if doc_id not in self.index:
            raise KeyError(f"Document with ID '{doc_id}' not found.")

        if doc_id != updated_document['id']:
            raise ValueError("The document's ID cannot be changed.")

        file_path = self._get_file_path(doc_id)

        with open(file_path, 'w', encoding=defaults.ENCODING) as file:
            json.dump(updated_document, file)

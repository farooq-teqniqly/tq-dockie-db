"""
This module provides the DocumentManager class for managing documents in a database.

This module provides functionality to create, read, update, and delete JSON documents
in a specified directory.

It uses the default encoding and filename extensions for the JSON files, and creates an
index file to keep track of the documents in the directory.
"""

import json
import os
import dockie.core.database_defaults as defaults


class DocumentManager:
    """
        A class for managing documents in a database.

        This class provides functionality to create, read, update, and delete
        JSON documents in a specified directory.
        It uses the default encoding and filename extensions for the JSON files,
        and creates an index file to keep track of the documents in the directory.

        Attributes:
            db_directory (str): The directory path where the documents are stored.
            index_file (str): The filename of the index file.
            index (dict): A dictionary containing the mapping of document IDs to their file paths.
    """

    def __init__(self, db_root, db_name):
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

    def write_file(self, document):
        """
            Write a document to the database.

            This function writes a document to the database.

            Args:
                document (dict): A dictionary containing the contents of the document.

            Returns:
                str: The ID of the inserted document.

            Raises:
                KeyError: If a document with the same ID already exists in the database.
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

    def update_file(self, doc_id, updated_document):
        """
            Update a document with the given ID in the database.

            This function updates a document with the specified ID in the database.

            Args:
                doc_id (str): The ID of the document to update.
                updated_document (dict): A dictionary containing the updated
                contents of the document.

            Returns:
                None

            Raises:
                KeyError: If a document with the given ID does not exist in the database.
                ValueError: If the ID of the updated document does not match the ID
                of the original document.
        """
        if doc_id not in self.index:
            raise KeyError(f"Document with ID '{doc_id}' not found.")

        if doc_id != updated_document['id']:
            raise ValueError("The document's ID cannot be changed.")

        file_path = self._get_file_path(doc_id)

        with open(file_path, 'w', encoding=defaults.ENCODING) as file:
            json.dump(updated_document, file)

    def read_file(self, doc_id):
        """
            Read a document with the given ID from the database.

            This function reads a document with the specified ID from the database.

            Args:
                doc_id (str): The ID of the document to read.

            Returns:
                dict: A dictionary containing the contents of the document.

            Raises:
                KeyError: If a document with the given ID does not exist in the database.
        """
        if doc_id not in self.index:
            raise KeyError(f"Document with ID '{doc_id}' not found.")

        file_path = self.index[doc_id]

        with open(file_path, 'r', encoding=defaults.ENCODING) as file:
            document = json.load(file)

        return document

    def delete_file(self, doc_id):
        """
            Delete a document with the given ID from the database.

            This function deletes a document with the specified ID from the database.

            Args:
                doc_id (str): The ID of the document to delete.

            Returns:
                None

            Raises:
                KeyError: If a document with the given ID does not exist in the database.
        """
        if doc_id not in self.index:
            raise KeyError(f"Document with ID '{doc_id}' not found.")

        file_path = self.index[doc_id]
        os.remove(file_path)
        del self.index[doc_id]
        self._save_index()

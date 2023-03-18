"""The DockieDb database module.

This module provides a simple document database implementation for managing JSON
documents using a file-based storage system. It supports basic CRUD operations
(create, read, update, and delete) on documents, which are stored in separate files
within a specified database directory.
"""

from dockie.core.document_manager import DocumentManager


class Database:
    """A document database class for managing and persisting JSON documents.

        This class provides a document database implementation for managing JSON
        documents using a file-based storage system. It supports basic CRUD operations
        (create, read, update, and delete) on documents, which are stored in separate files
        within a specified database directory.

        Attributes:
            document_manager (DocumentManager): The DocumentManager instance responsible
            for managing document files.
    """

    def __init__(self, db_root, db_name):
        """Initializes a new instance of the Database class. The database's location will be
        in the folder /[db_root]/[db_name]

                Args:
                    db_root (str): The path to the root directory containing all databases.
                    db_name (str): The name of the database.
        """
        self.document_manager = DocumentManager(db_root, db_name)

    def insert(self, document):
        """Inserts a new document into the database.

                Args:
                    document (dict): The document to insert.

                Returns:
                    str: The ID of the inserted document.

                Raises:
                    KeyError: If a document with the same ID already exists.
        """

        return self.document_manager.write_file(document)

    def get(self, doc_id):
        """Retrieves a document with the specified ID from the database.

                Args:
                    doc_id (str): The ID of the document to retrieve.

                Returns:
                    dict: The retrieved document.

                Raises:
                    KeyError: If a document with the specified ID does not exist.
        """
        return self.document_manager.read_file(doc_id)

    def delete(self, doc_id):
        """Delete a document from the database by its ID.

                Args:
                    doc_id (str): The unique ID of the document.

                Raises:
                    KeyError: If the document with the given ID is not found.
        """
        self.document_manager.delete_file(doc_id)

    def update(self, doc_id, updated_document):
        """Update a document in the database.

                Args:
                    doc_id (str): The unique ID of the document to update.
                    updated_document (dict): The updated document.

                Raises:
                    KeyError: If the document with the given ID is not found.
                    ValueError: If the document's ID is changed.
        """
        self.document_manager.update_file(doc_id, updated_document)

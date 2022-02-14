"""
Document container module.
"""
from typing import Dict

from dockie.core import errors, ensure
from dockie.core.document import Document, NoneDocument


class Container:
    """
    Document container class. A document container holds documents.
    """
    def __init__(self, name):
        """
        Creates a new Container instance.
        :param name: The container name.
        """
        ensure.not_none_or_whitespace(
            name, errors.ObjectCreateError("Container name not specified.")
        )

        self._name = name
        self._documents: Dict[str, Document] = {}

    def list_documents(self):
        """
        Lists the documents in the container.
        :return: The id's of the documents in the container.
        """
        return list(self._documents.keys())

    def add_document(self, document: Document):
        """
        Adds a document to the container.
        :param document: The document to add.
        """
        ensure.not_none(
            document, errors.ObjectCreateError("Document cannot be of type None.")
        )
        self._documents[document.get_id()] = document

    def get_document(self, document_id) -> Document:
        """
        Retrieves a document by its id.
        :param document_id: The document id.
        :return: The document. If the document was not found,
        a NoneDocument instance is returned instead.
        """
        ensure.id_specified(
            document_id, errors.ObjectReadError("Document id not specified.")
        )

        document = self._documents.get(document_id)

        if document is None:
            return NoneDocument(document_id, {})

        return document

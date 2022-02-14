"""
Document module.
"""
from dockie.core import errors, ensure


class Document:
    """Document class. A document is the basic storage primitive in a document database."""

    def __init__(self, document_id, data: dict):
        """
        Creates a Document instance.
        :param document_id: The document id.
        :param data: The document data.
        """
        ensure.id_specified(
            document_id, errors.ObjectCreateError("Document id not specified.")
        )

        ensure.not_none(
            data,
            errors.ObjectCreateError(
                "Document data cannot be of type None. "
                "To create a document with no data, pass an empty dict, '{}'."
            ),
        )

        self._document_id = document_id
        self._data = data

    def get_id(self) -> str:
        """
        Retrieves the document's id.
        :return: The document id.
        """
        return self._document_id

    def get_data(self) -> dict:
        """
        Retrieves the document's data.
        :return: The document's data.
        """
        return self._data


class NoneDocument(Document):
    """
    Represents a document that doesn't exist.
    """

from typing import Dict

from dockie.core import errors, ensure
from dockie.core.document import Document, NoneDocument


class Container(object):
    def __init__(self, name):
        ensure.not_none_or_whitespace(
            name, errors.ObjectCreateError("Container name not specified.")
        )

        self._name = name
        self._documents: Dict[str, Document] = {}

    def list_documents(self):
        return list(self._documents.keys())

    def add_document(self, document: Document):
        ensure.not_none(
            document, errors.ObjectCreateError("Document cannot be of type None.")
        )
        self._documents[document.get_id()] = document

    def get_document(self, document_id) -> Document:
        ensure.id_specified(
            document_id, errors.ObjectReadError("Document id not specified.")
        )

        document = self._documents.get(document_id)

        if document is None:
            return NoneDocument(document_id, {})

        return document

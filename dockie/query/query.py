"""
Query module.
"""
from abc import ABC, abstractmethod
from typing import Union, List
import dictquery as dq
from dockie.core.container import Container
from dockie.core import ensure
from dockie.core import errors
from dockie.core.document import Document, NoneDocument


class DocumentQuery(ABC):
    """
    Represents a document query. This class is the base class for
    all document query types.
    """

    def execute(self, container: Container, **kwargs):
        """
        Executes the document query.
        :param container: The container to query.
        :param kwargs: Additional keyword arguments to the query.
        :return: The query result.
        """
        ensure.not_none(
            container, errors.ObjectCreateError("Container name not specified.")
        )
        return self.on_execute(container, **kwargs)

    @abstractmethod
    def on_execute(self, container: Container, **kwargs):  # pragma: no cover
        """
        Called by derived classes. This method contains type specific query logic.
        :param container: The container to query.
        :param kwargs: Additional keyword arguments to the query.
        """


class DocumentIdQuery(DocumentQuery):
    """
    Represents a document id query.
    """

    def on_execute(
            self, container: Container, **kwargs
    ) -> Union[Document, NoneDocument]:
        document_id = kwargs.get("document_id")

        ensure.id_specified(
            document_id, errors.QueryError("Document id not specified.")
        )

        return container.get_document(document_id)


class DocumentAttributeQuery(DocumentQuery):
    """
    Represents a document attribute query,
    """

    def on_execute(self, container: Container, **kwargs) -> List[Document]:
        documents = []
        query = kwargs.get("query")
        ensure.not_none(query, errors.QueryError("Query string not specified."))

        for document_id in container.list_documents():
            document = container.get_document(document_id)

            if dq.match(document.get_data(), query):
                documents.append(document)

        return documents

from abc import ABC, abstractmethod
from typing import Union, List

from dockie.core.container import Container
import dockie.core.ensure as ensure
import dockie.core.errors as errors
import dictquery as dq
from dockie.core.document import Document, NoneDocument


class DocumentQuery(ABC):
    def execute(self, container: Container, **kwargs):
        ensure.not_none(
            container, errors.ObjectCreateError("Container name not specified.")
        )
        return self.on_execute(container, **kwargs)

    @abstractmethod
    def on_execute(self, container: Container, **kwargs):  # pragma: no cover
        pass


class DocumentIdQuery(DocumentQuery):
    def on_execute(
        self, container: Container, **kwargs
    ) -> Union[Document, NoneDocument]:
        document_id = kwargs.get("document_id")

        ensure.id_specified(
            document_id, errors.QueryError("Document id not specified.")
        )

        return container.get_document(document_id)


# https://pypi.org/project/dictquery/


class DocumentAttributeQuery(DocumentQuery):
    def on_execute(self, container: Container, **kwargs) -> List[Document]:
        documents = []
        query = kwargs.get("query")
        ensure.not_none(query, errors.QueryError("Query string not specified."))

        for document_id in container.list_documents():
            document = container.get_document(document_id)

            if dq.match(document.get_data(), query):
                documents.append(document)

        return documents

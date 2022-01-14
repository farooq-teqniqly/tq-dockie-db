from abc import ABC, abstractmethod
from typing import Union

from dockie.core.container import Container
import dockie.core.ensure as ensure
import dockie.core.errors as errors
from dockie.core.document import Document, NoneDocument


class DocumentQuery(ABC):
    def execute(self, container: Container, **kwargs):
        ensure.not_none(
            container, errors.ObjectCreateError("Container name not specified.")
        )
        return self.on_execute(container, **kwargs)

    @abstractmethod
    def on_execute(self, container: Container, **kwargs):
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

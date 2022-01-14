from typing import Dict, List


class Database(object):
    def __init__(self, name):
        if not name or len(name) == 0:
            raise ValueError("Specify the database name.")

        self._name = name
        self._containers: Dict[str, Container] = {}

    def get_name(self) -> str:
        return self._name

    def list_containers(self) -> List[str]:
        return list(self._containers.keys())

    def add_container(self, name):
        if self._containers.get(name) is not None:
            raise ValueError(
                f"The container named '{name}' already exists. Container names must be unique within a database."
            )

        self._containers[name] = Container(name)

    def get_container(self, container_name: str):
        container = self._containers.get(container_name)
        return container


class Document(object):
    def __init__(self, document_id: str, data: dict):
        if not document_id or len(document_id) == 0:
            raise ValueError("Specify the document_id.")

        self.document_id = document_id
        self.data = data


class Container(object):
    def __init__(self, name):
        if not name or len(name) == 0:
            raise ValueError("Specify the database name.")

        self._name = name
        self._documents: Dict[str, Document] = {}

    def list_documents(self):
        return list(self._documents.keys())

    def add_document(self, document: Document):
        if document is None:
            raise ValueError("Document cannot be of type None.")

        self._documents[document.document_id] = document

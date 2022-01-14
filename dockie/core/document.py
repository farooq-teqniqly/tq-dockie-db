from dockie.core import errors, ensure


class Document(object):
    def __init__(self, document_id, data: dict):
        ensure.id_specified(
            document_id, errors.ObjectCreateError("Document id not specified.")
        )

        ensure.not_none(
            data,
            errors.ObjectCreateError(
                "Document data cannot be of type None. To create a document with no data, pass an empty dict, '{}'."
            ),
        )

        self._document_id = document_id
        self._data = data

    def get_id(self) -> str:
        return self._document_id

    def get_data(self) -> dict:
        return self._data


class NoneDocument(Document):
    pass

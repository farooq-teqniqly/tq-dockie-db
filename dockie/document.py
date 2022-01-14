from dockie import ensure, errors


class Document(object):
    def __init__(self, document_id: str, data: dict):
        ensure.not_null_or_whitespace(
            document_id, errors.ObjectCreateError("Specify the document id.")
        )

        ensure.not_null(
            data,
            errors.ObjectCreateError(
                "Document data cannot be of type None. To create a document with no data, pass an empty dict, '{}'."
            ),
        )

        self._document_id = document_id
        self._data = data

    def get_document_id(self) -> str:
        return self._document_id

    def get_data(self) -> dict:
        return self._data

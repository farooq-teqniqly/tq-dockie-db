from dockie.core import errors, ensure


class Document(object):
    def __init__(self, document_id, data: dict):
        if type(document_id) == str:
            ensure.not_none_or_whitespace(
                document_id, errors.ObjectCreateError("Specify the document id.")
            )
        elif type(document_id) == int:
            ensure.not_none(
                document_id, errors.ObjectCreateError("Specify the document id.")
            )
        else:
            raise errors.ObjectCreateError(
                "Supported document id types are 'int' and 'str'."
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

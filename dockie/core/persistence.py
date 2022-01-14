import os.path
import pickle

from dockie.core import ensure, errors
from dockie.core.database import Database


def persist_to_file(db: Database, filename: str, overwrite=False):
    ensure.not_none(db, errors.PersistenceError("Database not specified."))
    ensure.not_none_or_whitespace(
        filename, errors.PersistenceError("File name not specified.")
    )

    if os.path.exists(filename) and not overwrite:
        raise errors.PersistenceError(
            f"File '{filename}' exists and overwrite is False, therefore the database will not be persisted."
        )

    pickle.dump(db, open(filename, "wb"))


def load_from_file(filename: str) -> Database:
    ensure.not_none_or_whitespace(
        filename, errors.PersistenceError("File name not specified.")
    )

    if not os.path.exists(filename):
        raise errors.PersistenceError(f"The file '{filename}' was not found.")

    return pickle.load(open(filename, "rb"))

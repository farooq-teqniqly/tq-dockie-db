"""
Persistence module.
"""
import os.path
import pickle

from dockie.core import ensure, errors
from dockie.core.database import Database


def persist_to_file(database: Database, filename: str, overwrite=False):
    """
    Persists the database to a pickle file.
    :param database: The database.
    :param filename: The file name.
    :param overwrite: When True and the file exists, the file is overwritten.
    When False and the file exists, an error is raised.
    """
    ensure.not_none(database, errors.PersistenceError("Database not specified."))
    ensure.not_none_or_whitespace(
        filename, errors.PersistenceError("File name not specified.")
    )

    if os.path.exists(filename) and not overwrite:
        raise errors.PersistenceError(
            f"File '{filename}' exists and overwrite is False, "
            f"therefore the database will not be persisted."
        )

    with open(filename, "wb") as file:
        pickle.dump(database, file)


def load_from_file(filename: str) -> Database:
    """
    Loads the database from a pickle file.
    :param filename: The file name.
    :return: The Database instance.
    """
    ensure.not_none_or_whitespace(
        filename, errors.PersistenceError("File name not specified.")
    )

    if not os.path.exists(filename):
        raise errors.PersistenceError(f"The file '{filename}' was not found.")

    return pickle.load(open(filename, "rb"))

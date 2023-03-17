import json
import os
import dockie.core.database_defaults as defaults

class FileManager:
    def __init__(self, db_root, db_name):
        self.db_directory = os.path.join(db_root, db_name)

        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)

        self.index_file = os.path.join(self.db_directory, f'{db_name}.json')
        self.index = self._load_index()

    def _load_index(self):
        """Loads the index from the index file, or creates an empty index if the file doesn't exist.

                Returns:
                    dict: The index dictionary.
        """
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r', encoding=defaults.ENCODING) as file:
                index = json.load(file)
        else:
            index = {}
        return index

    def _save_index(self):
        """Saves the index to the index file."""
        with open(self.index_file, 'w', encoding=defaults.ENCODING) as file:
            json.dump(self.index, file)

    def _get_file_path(self, doc_id):
        """Generates the file path for a document with the given ID.

                Args:
                    doc_id (str): The ID of the document.

                Returns:
                    str: The file path for the document.
        """
        return os.path.join(self.db_directory, f'{doc_id}.json')
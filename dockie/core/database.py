"""
Database module.
"""
from typing import Dict, List

from dockie.core.container import Container
from dockie.core import errors, ensure


class Database:
    """Database class. A database holds one or more Container instances."""

    def __init__(self):
        self._containers: Dict[str, Container] = {}

    def list_containers(self) -> List[str]:
        """
        List the containers in the database.
        :return: A list of the container names.
        """
        return list(self._containers.keys())

    def add_container(self, name):
        """
        Add a container to the database.
        :param name: The container name.
        """
        ensure.not_none_or_whitespace(
            name, errors.ObjectCreateError("Container name not specified.")
        )

        if self._containers.get(name) is not None:
            raise errors.ObjectCreateError(
                f"The container named '{name}' already exists. "
                f"Container names must be unique within a database."
            )

        self._containers[name] = Container(name)

    def get_container(self, name: str):
        """
        Retrieve a container by its name.
        :param name: The container name.
        :return: The container.
        """
        ensure.not_none_or_whitespace(
            name, errors.ObjectReadError("Container name not specified.")
        )

        container = self._containers.get(name)

        if container is None:
            raise errors.ObjectNotFoundError(f"Container '{name}' was not found.")

        return container

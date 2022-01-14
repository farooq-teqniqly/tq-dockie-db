from typing import Dict, List

from dockie.container import Container
from dockie import errors, ensure


class Database(object):
    def __init__(self, name):
        ensure.not_none_or_whitespace(
            name, errors.ObjectCreateError("Database name not specified.")
        )
        self._name = name
        self._containers: Dict[str, Container] = {}

    def get_name(self) -> str:
        return self._name

    def list_containers(self) -> List[str]:
        return list(self._containers.keys())

    def add_container(self, name):
        ensure.not_none_or_whitespace(
            name, errors.ObjectCreateError("Container name not specified.")
        )

        if self._containers.get(name) is not None:
            raise errors.ObjectCreateError(
                f"The container named '{name}' already exists. Container names must be unique within a database."
            )

        self._containers[name] = Container(name)

    def get_container(self, name: str):
        ensure.not_none_or_whitespace(
            name, errors.ObjectReadError("Container name not specified.")
        )

        container = self._containers.get(name)

        if container is None:
            raise errors.ObjectNotFoundError(f"Container '{name}' was not found.")

        return container

from __future__ import annotations

from src.exceptions import UnknownLoader
from src.loaders.base_loader import BaseLoader
from src.loaders.mysql_loader import MySQLLoader
from src.loaders.postgres_loader import PostgresLoader

__all__ = ["get_loader"]

_REGISTRY: dict[str, type[BaseLoader]] = {
    "postgres": PostgresLoader,
    "pg":       PostgresLoader,
    "mysql":    MySQLLoader,
}


def get_loader(db_type: str) -> BaseLoader:
    cls = _REGISTRY.get(db_type.lower())
    if cls is None:
        raise UnknownLoader(db_type, list(_REGISTRY.keys()))
    return cls()

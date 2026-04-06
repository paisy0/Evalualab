from __future__ import annotations

from abc import ABC, abstractmethod

__all__ = ["BaseLoader"]


class BaseLoader(ABC):

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def fetch(self, query: str) -> list[dict]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc):
        self.close()

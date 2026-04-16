"""Abstract base class for format handlers."""

from abc import ABC, abstractmethod


class BaseFormat(ABC):
    """Base class for all format handlers."""

    @abstractmethod
    def load(self, content: str) -> object:
        """Parse string content into Python data structure."""

    @abstractmethod
    def dump(self, data: object, pretty: bool = False) -> str:
        """Serialize Python data structure to string."""

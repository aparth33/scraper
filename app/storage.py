from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    def save(self, data: dict):
        """Save data to the storage backend."""
        pass

    @abstractmethod
    def load(self) -> list:
        """Load data from the storage backend."""
        pass

    @abstractmethod
    def update(self, data: dict):
        """update data to the storage backend."""
        pass

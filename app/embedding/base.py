
from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Interface for text embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Convert one text into an embedding vector."""
        raise NotImplementedError

    @abstractmethod
    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Convert multiple texts into embedding vectors."""
        raise NotImplementedError
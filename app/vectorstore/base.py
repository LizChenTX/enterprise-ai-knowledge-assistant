
from abc import ABC, abstractmethod

from app.models.chunk import Chunk
from app.vectorstore.models import VectorSearchResult


class VectorStore(ABC):
    """Abstract interface for vector storage and similarity search."""

    @abstractmethod
    def add(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        """Store chunks and their corresponding embedding vectors."""
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        """Return the most similar chunks, highest score first."""
        raise NotImplementedError

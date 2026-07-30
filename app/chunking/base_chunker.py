from abc import ABC, abstractmethod

from app.models.chunk import Chunk
from app.models.document import Document


class BaseChunker(ABC):
    """
    Abstract interface for all chunking strategies.
    """

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split a document into chunks.
        """
        raise NotImplementedError
from abc import ABC, abstractmethod

from app.models.chunk import Chunk
from app.models.document import Document
from app.models.section import Section


class BaseChunker(ABC):

    @abstractmethod
    def chunk(
        self,
        document: Document,
        sections: list[Section],
    ) -> list[Chunk]:
        """
        Split document sections into retrievable chunks.
        """
        ...
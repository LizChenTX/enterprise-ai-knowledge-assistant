from app.chunking.base_chunker import BaseChunker
from app.config.chunking_config import ChunkConfig
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.section import Section


DEFAULT_SEPARATORS = [
    "\n\n",
    "\n",
    ". ",
    " ",
]


class RecursiveChunker(BaseChunker):

    def __init__(
        self,
        config: ChunkConfig | None = None,
    ):
        self.config = config or ChunkConfig()

    def chunk(
        self,
        document: Document,
        sections: list[Section],
    ) -> list[Chunk]:

        chunks: list[Chunk] = []
        chunk_index = 0

        for section in sections:
            text_chunks = self._split_recursively(
                section.content,
                DEFAULT_SEPARATORS,
            )

            for text in text_chunks:
                start_offset = document.content.find(text)
                end_offset = start_offset + len(text)
                chunks.append(
                    Chunk(
                        # Chunk model
                        # required fields
                        document_id=document.id,
                        chunk_index=chunk_index,
                        content=text,
                        section_path=section.heading_path.copy(),
                        metadata=document.metadata,
                        start_offset=start_offset,
                        end_offset=end_offset,
                    )
                )

                chunk_index += 1

        return chunks

    def _split_recursively(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:
        text = text.strip()

        if not text:
            return []

        if len(text) <= self.config.chunk_size:
            return [text]

        if not separators:
            return self._split_by_characters(text)

        separator = separators[0]
        remaining_separators = separators[1:]

        if separator not in text:
            return self._split_recursively(
                text,
                remaining_separators,
            )

        parts = [
            part.strip()
            for part in text.split(separator)
            if part.strip()
        ]

        chunks: list[str] = []

        for part in parts:
            if len(part) <= self.config.chunk_size:
                chunks.append(part)
            else:
                chunks.extend(
                    self._split_recursively(
                        part,
                        remaining_separators,
                    )
                )

        return chunks

    def _split_by_characters(
        self,
        text: str,
    ) -> list[str]:
        chunk_size = self.config.chunk_size

        return [
            text[i:i + chunk_size]
            for i in range(
                0,
                len(text),
                chunk_size,
            )
        ]
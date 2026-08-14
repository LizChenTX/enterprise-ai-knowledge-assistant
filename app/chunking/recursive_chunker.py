from app.models.chunk import Chunk
from app.models.document import Document
from app.models.section import Section

DEFAULT_SEPARATORS = [
    "\n\n",
    "\n",
    ". ",
    " ",
]

class RecursiveChunker:

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

            paragraphs = self._split_paragraphs(
                section.content
            )

            for paragraph in paragraphs:

                start_offset = document.content.find(
                    paragraph
                )

                end_offset = (
                    start_offset + len(paragraph)
                )

                chunks.append(
                    Chunk(
                        document_id=document.id,
                        chunk_index=chunk_index,
                        content=paragraph,
                        metadata=document.metadata,
                        start_offset=start_offset,
                        end_offset=end_offset,
                        section_path=section.heading_path.copy(),
                    )
                )

                chunk_index += 1

        return chunks

    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:
        return [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]
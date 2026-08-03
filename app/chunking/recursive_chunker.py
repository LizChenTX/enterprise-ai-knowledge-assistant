from app.chunking.base_chunker import BaseChunker
from app.config.chunking_config import ChunkingConfig
from app.models.chunk import Chunk
from app.models.document import Document


class RecursiveChunker(BaseChunker):
    """
    Recursive chunking strategy.

    First version:
    split document by paragraphs.
    """

    def chunk(
        self,
        document: Document,
        config: ChunkingConfig,
    ) -> list[Chunk]:

        paragraphs = self._split_paragraphs(
            document.content
        )

        chunks = []

        current_index = 0

        for paragraph in paragraphs:

            if not paragraph.strip():
                continue

            chunk = Chunk(
                document_id=document.id,
                chunk_index=current_index,
                content=paragraph,
                metadata=document.metadata,
                start_offset=0,
                end_offset=len(paragraph),
                token_count=0,
            )

            chunks.append(chunk)

            current_index += 1

        return chunks


    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:

        return text.split("\n\n")
    
    def _parse_markdown_sections(
        self,
        text: str,
    ) -> list[tuple[str | None, str]]:
        """
        Parse a markdown document into (section, paragraph) pairs.
        """

        sections: list[tuple[str | None, str]] = []

        current_section: str | None = None

        paragraphs = text.split("\n\n")

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            if paragraph.startswith("#"):

                current_section = paragraph.lstrip("#").strip()

                continue

            sections.append(
                (
                    current_section,
                    paragraph,
                )
            )

        return sections
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
            # text_chunks = self._split_recursively(
            #     section.content,
            #     DEFAULT_SEPARATORS,
            # )

            text_units = self._split_recursively(
                section.content,
                DEFAULT_SEPARATORS,
            )

            packed_chunks = self._pack_chunks_with_overlap(
                text_units
            )

            for units in packed_chunks:
                text = self._render_chunk_units(units)
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

    def _pack_chunks(
        self,
        units: list[str],
    ) -> list[str]:

        chunks: list[str] = []
        current_units: list[str] = []
        current_length = 0

        for unit in units:
            unit_length = len(unit)

            separator_length = 2 if current_units else 0

            if (
                current_units
                and current_length
                + separator_length
                + unit_length
                > self.config.chunk_size
            ):
                chunks.append(
                    "\n\n".join(current_units)
                )

                current_units = [unit]
                current_length = unit_length

            else:
                current_units.append(unit)

                current_length += (
                    separator_length + unit_length
                )

        if current_units:
            chunks.append(
                "\n\n".join(current_units)
            )

        return chunks

    def _pack_chunks_with_overlap(
        self,
        units: list[str],
    ) -> list[list[str]]:
        """
        Pack semantic units into chunks while preserving
        complete semantic units as overlap.

        Example with overlap=1:

            [A, B, C, D]

        becomes:

            [A, B]
            [B, C]
            [C, D]
        """
        if not units:
            return []

        chunks: list[list[str]] = []
        current: list[str] = []
        current_length = 0

        for unit in units:
            unit_length = len(unit)
            separator_length = 2 if current else 0

            # If adding this unit would exceed chunk_size,
            # finalize the current chunk.
            if (
                current
                and current_length
                + separator_length
                + unit_length
                > self.config.chunk_size
            ):
                chunks.append(current)

                # Preserve complete semantic units for overlap.
                overlap_units: list[str] = []
                overlap_length = 0

                for previous_unit in reversed(current):
                    if len(overlap_units) >= self.config.chunk_overlap:
                        break

                    previous_length = len(previous_unit)

                    if (
                        overlap_length
                        + previous_length
                        + (2 if overlap_units else 0)
                        <= self.config.chunk_size
                    ):
                        overlap_units.insert(0, previous_unit)
                        overlap_length += (
                            previous_length
                            + (2 if overlap_units else 0)
                        )
                    else:
                        break

                current = overlap_units + [unit]

                current_length = sum(
                    len(item) for item in current
                ) + 2 * (len(current) - 1)

            else:
                current.append(unit)
                current_length += separator_length + unit_length

        if current:
            chunks.append(current)

        return chunks

    def _render_chunk_units(
        self,
        units: list[str],
    ) -> str:
        """
        Convert semantic units into the final chunk text.
        """
        return "\n\n".join(units)
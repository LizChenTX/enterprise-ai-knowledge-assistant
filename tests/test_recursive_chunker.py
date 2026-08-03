from app.chunking.recursive_chunker import RecursiveChunker
from app.config.chunking_config import ChunkingConfig
from app.models.document import Document
from app.models.metadata import Metadata
from app.models.enums import (
    DocumentSource,
    DocumentType,
)


def test_recursive_chunker():

    document = Document(
        content=(
            "# Authentication\n\n"
            "JWT token explanation.\n\n"
            "OAuth explanation."
        ),
        metadata=Metadata(
            title="security",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    chunker = RecursiveChunker()

    chunks = chunker.chunk(
        document,
        ChunkingConfig(),
    )

    assert len(chunks) == 3

    assert chunks[0].chunk_index == 0

    assert (
        chunks[0].content
        ==
        "# Authentication"
    )

    assert chunks[1].content == (
        "JWT token explanation."
    )
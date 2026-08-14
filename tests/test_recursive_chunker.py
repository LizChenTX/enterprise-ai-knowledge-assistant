from app.chunking.recursive_chunker import RecursiveChunker
from app.config.chunking_config import ChunkingConfig
from app.models.document import Document
from app.models.metadata import Metadata
from app.models.enums import (
    DocumentSource,
    DocumentType,
)
from app.chunking.recursive_chunker import RecursiveChunker
from app.models.section import Section
from app.parsers.markdown_parser import MarkdownParser


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

    parser = MarkdownParser()
    sections = parser.parse(document.content)

    chunker = RecursiveChunker()

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) == 2

    assert chunks[0].content == "JWT token explanation."
    assert chunks[0].section_path == [
        "Authentication"
    ]

    assert chunks[1].content == "OAuth explanation."
    assert chunks[1].section_path == [
        "Authentication"
    ]

def test_chunk_sections_by_paragraph():
    document = Document(
        content=(
            "JWT token explanation.\n\n"
            "OAuth explanation.\n\n"
            "PostgreSQL information."
        ),
        metadata=Metadata(
            title="test",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    sections = [
        Section(
            heading_path=["Authentication"],
            content=(
                "JWT token explanation.\n\n"
                "OAuth explanation."
            ),
        ),
        Section(
            heading_path=["Database"],
            content="PostgreSQL information.",
        ),
    ]

    chunker = RecursiveChunker()

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) == 3

    assert chunks[0].content == "JWT token explanation."
    assert chunks[0].section_path == [
        "Authentication"
    ]

    assert chunks[1].content == "OAuth explanation."
    assert chunks[1].section_path == [
        "Authentication"
    ]

    assert chunks[2].content == "PostgreSQL information."
    assert chunks[2].section_path == [
        "Database"
    ]

def test_chunk_preserves_section_hierarchy():
    document = Document(
        content="JWT tokens expire after one hour.",
        metadata=Metadata(
            title="security",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    sections = [
        Section(
            heading_path=[
                "Authentication",
                "JWT",
                "Expiration",
            ],
            content="JWT tokens expire after one hour.",
        )
    ]

    chunker = RecursiveChunker()

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) == 1

    assert chunks[0].section_path == [
        "Authentication",
        "JWT",
        "Expiration",
    ]

    assert chunks[0].content == (
        "JWT tokens expire after one hour."
    )

def test_large_paragraph_is_split_recursively():
    section = Section(
        heading_path=["Authentication"],
        content=(
            "This is the first sentence. "
            "This is the second sentence. "
            "This is the third sentence."
        ),
    )

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=40,
            chunk_overlap=0,
        )
    )

    chunks = chunker.chunk([section])

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 40
        for chunk in chunks
    )

    assert all(
        chunk.section_path == ["Authentication"]
        for chunk in chunks
    )

def test_fallback_to_word_split():
    section = Section(
        heading_path=["Test"],
        content=(
            "one two three four five six "
            "seven eight nine ten eleven twelve"
        ),
    )

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=15,
            chunk_overlap=0,
        )
    )

    chunks = chunker.chunk([section])

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 15
        for chunk in chunks
    )
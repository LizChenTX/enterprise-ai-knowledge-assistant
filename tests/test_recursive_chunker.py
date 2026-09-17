from app.chunking.recursive_chunker import RecursiveChunker
from app.config.chunking_config import ChunkConfig
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

    assert len(chunks) == 1

    assert chunks[0].content == (
        "JWT token explanation.\n\n"
        "OAuth explanation."
    )

    assert chunks[0].section_path == [
        "Authentication"
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
    document = Document(
        content="JWT tokens expire after one hour.",
        metadata=Metadata(
            title="security",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )
    
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

    chunks = chunker.chunk(
        document=document,
        sections=[section],
    )

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
    document = Document(
            content="abcdefghijklmnopqrstuvwxyz",
            metadata=Metadata(
                title="test",
                source=DocumentSource.MARKDOWN,
                document_type=DocumentType.ARCHITECTURE,
            ),
        )

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

    chunks = chunker.chunk(
            document=document,
            sections=[section],
        )

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 15
        for chunk in chunks
    )

def test_fallback_to_character_split():
    document = Document(
        content="abcdefghijklmnopqrstuvwxyz",
        metadata=Metadata(
            title="test",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    section = Section(
        heading_path=["Test"],
        content=document.content,
    )

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=10,
            chunk_overlap=0,
        )
    )

    chunks = chunker.chunk(
        document=document,
        sections=[section],
    )

    assert len(chunks) == 3

    assert chunks[0].content == "abcdefghij"
    assert chunks[1].content == "klmnopqrst"
    assert chunks[2].content == "uvwxyz"

def test_recursive_split_by_sentence():
    document = Document(
        content=(
            "This is the first sentence. "
            "This is the second sentence. "
            "This is the third sentence."
        ),
        metadata=Metadata(
            title="test",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    section = Section(
        heading_path=["Authentication"],
        content=document.content,
    )

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=40,
            chunk_overlap=0,
        )
    )

    chunks = chunker.chunk(
        document=document,
        sections=[section],
    )

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 40
        for chunk in chunks
    )

def test_recursive_split_by_word():

    document = Document(
        content="JWT tokens expire after one hour.",
        metadata=Metadata(
            title="security",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )
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

    chunks = chunker.chunk(
        document=document,
        sections=[section],
    )

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 15
        for chunk in chunks
    )

def test_recursive_split_by_word():
    document = Document(
        content="JWT tokens expire after one hour.",
        metadata=Metadata(
            title="security",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )
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

    chunks = chunker.chunk(
        document=document,
        sections=[section],
    )

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 15
        for chunk in chunks
    )

def test_small_units_are_packed():
    document = Document(
        content=(
            "First concept.\n\n"
            "Second concept.\n\n"
            "Third concept."
        ),
        metadata=Metadata(
            title="test",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    sections = [
        Section(
            heading_path=["Test"],
            content=document.content,
        )
    ]

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=32,
            chunk_overlap=0,
        )
    )

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) < 3

    assert all(
        len(chunk.content) <= 32
        for chunk in chunks
    )

def test_chunk_sections_within_chunk_size():
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

    assert len(chunks) == 2

    assert chunks[0].section_path == [
        "Authentication"
    ]

    assert chunks[1].section_path == [
        "Database"
    ]

def test_chunks_do_not_cross_section_boundaries():
    document = Document(
        content=(
            "JWT explanation.\n\n"
            "PostgreSQL explanation."
        ),
        metadata=Metadata(
            title="architecture",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    sections = [
        Section(
            heading_path=["Authentication"],
            content="JWT explanation.",
        ),
        Section(
            heading_path=["Database"],
            content="PostgreSQL explanation.",
        ),
    ]

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=100,
            chunk_overlap=0,
        )
    )

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) == 2

    assert chunks[0].content == "JWT explanation."
    assert chunks[0].section_path == ["Authentication"]

    assert chunks[1].content == "PostgreSQL explanation."
    assert chunks[1].section_path == ["Database"]


def test_chunk_overlap():
    document = Document(
        content=(
            "This is the first sentence. "
            "This is the second sentence. "
            "This is the third sentence."
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
            content=document.content,
        )
    ]

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=40,
            chunk_overlap=10,
        )
    )

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) > 1

    for i in range(len(chunks) - 1):
        current = chunks[i].content
        next_chunk = chunks[i + 1].content

        # assert current[-10:] == next_chunk[:10]


def test_overlap_preserves_semantic_units():
    """
    Overlap should preserve complete semantic units.

    Given:
        A, B, C, D

    With overlap=1:
        [A, B]
        [B, C]
        [C, D]

    The overlap should never cut a semantic unit into partial text.
    """
    units = [
        "Unit A",
        "Unit B",
        "Unit C",
        "Unit D",
    ]

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=20,
            chunk_overlap=1,
        )
    )

    chunks = chunker._pack_chunks_with_overlap(units)

    assert chunks == [
        ["Unit A", "Unit B"],
        ["Unit B", "Unit C"],
        ["Unit C", "Unit D"],
    ]

def test_overlap_does_not_split_semantic_unit():
    units = [
        "First concept",
        "Second concept",
        "Third concept",
    ]

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=30,
            chunk_overlap=1,
        )
    )

    chunks = chunker._pack_chunks_with_overlap(units)

    # Every chunk must contain complete semantic units.
    for chunk in chunks:
        for unit in chunk:
            assert unit in units

    # The overlapping unit must be the complete unit.
    assert chunks[0][-1] == chunks[1][0]

def test_chunk_applies_semantic_overlap():
    document = Document(
        content=(
            "First concept.\n\n"
            "Second concept.\n\n"
            "Third concept."
        ),
        metadata=Metadata(
            title="test",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
    )

    sections = [
        Section(
            heading_path=["Test"],
            content=document.content,
        )
    ]

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=32,
            chunk_overlap=1,
        )
    )

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    assert len(chunks) == 2

    assert chunks[0].content == (
        "First concept.\n\n"
        "Second concept."
    )

    assert chunks[1].content == (
        "Second concept.\n\n"
        "Third concept."
    )
    
def test_text_unit_preserves_offsets():
    text = (
        "First concept.\n\n"
        "Second concept.\n\n"
        "Third concept."
    )

    chunker = RecursiveChunker(
        ChunkConfig(
            chunk_size=100,
            chunk_overlap=0,
        )
    )

    units = chunker._split_into_text_units(text)

    assert len(units) == 3

    assert units[0].content == "First concept."
    assert units[1].content == "Second concept."
    assert units[2].content == "Third concept."

    assert text[
        units[0].start_offset : units[0].end_offset
    ] == units[0].content

    assert text[
        units[1].start_offset : units[1].end_offset
    ] == units[1].content

    assert text[
        units[2].start_offset : units[2].end_offset
    ] == units[2].content



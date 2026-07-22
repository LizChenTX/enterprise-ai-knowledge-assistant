from pathlib import Path

import pytest

from app.ingestion.markdown_loader import MarkdownLoader


def test_load_markdown_file():
    loader = MarkdownLoader()

    document = loader.load(
        Path("sample_docs/architecture.md")
    )

    assert document.content.startswith("# Authentication")

    assert document.metadata.title == "architecture"

    assert document.metadata.source == "markdown"

    assert document.metadata.document_type == "markdown"

def test_file_not_found():
    loader = MarkdownLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("abc.md")

def test_file_not_found():
    loader = MarkdownLoader()

    with pytest.raises(FileNotFoundError):
        loader.load(Path("abc.md"))
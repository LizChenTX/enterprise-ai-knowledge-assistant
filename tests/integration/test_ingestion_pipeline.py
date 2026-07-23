from pathlib import Path

import pytest

from app.ingestion.markdown_loader import MarkdownLoader
from app.models.document import Document
from app.models.metadata import Metadata

@pytest.mark.integration
def test_markdown_ingestion_pipeline():
    """
    Verify complete markdown ingestion flow:

    Markdown file
        ->
    MarkdownLoader
        ->
    Document
        ->
    Metadata
    """

    # Arrange
    file_path = Path(
        "sample_docs/architecture.md"
    )

    loader = MarkdownLoader()

    # Act
    document = loader.load(file_path)

    # Assert
    assert isinstance(document, Document)

    assert document.content is not None
    assert len(document.content) > 0

    assert isinstance(
        document.metadata,
        Metadata
    )

    assert document.metadata.title == "architecture"

    assert document.metadata.source == "markdown"
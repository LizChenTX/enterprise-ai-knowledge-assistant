from pathlib import Path

from app.models.document import Document
from app.models.metadata import Metadata


class MarkdownLoader:
    """
    Load a Markdown file and convert it into a Document.

    Responsibilities:
        - Read markdown content from disk
        - Create a Metadata object
        - Return a standardized Document

    It does NOT:
        - Chunk the document
        - Generate embeddings
        - Store anything
    """

    def load(self, file_path: Path) -> Document:
        """
        Load a markdown file.

        Args:
            file_path: Path to a markdown file.

        Returns:
            A Document object.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        if file_path.suffix.lower() != ".md":
            raise ValueError("Only Markdown (.md) files are supported.")

        content = file_path.read_text(encoding="utf-8")

        metadata = Metadata(
            title=file_path.stem,
            source="markdown",
            document_type="markdown",
        )

        return Document(
            content=content,
            metadata=metadata,
        )
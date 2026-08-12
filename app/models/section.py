from pydantic import BaseModel, Field


class Section(BaseModel):
    """
    A logical section extracted from a document.

    A section preserves document structure before the content
    is split into smaller retrievable chunks.
    """

    title: str | None = Field(
        default=None,
        description="Section title, if available.",
    )

    content: str = Field(
        description="Content belonging to this section.",
    )
from pydantic import BaseModel, Field


class Section(BaseModel):
    """
    A logical section extracted from a document.

    It preserves document structure before chunking.
    """

    title: str | None = Field(
        default=None,
        description="Section title.",
    )

    content: str = Field(
        description="Section content.",
    )
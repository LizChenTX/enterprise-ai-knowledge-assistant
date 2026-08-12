from pydantic import BaseModel, Field


class Section(BaseModel):
    """
    A logical section extracted from a document.

    The heading path preserves the hierarchical structure
    of the source document while keeping sections flat for
    downstream processing.
    """

    heading_path: list[str] = Field(
        default_factory=list,
        description="Hierarchical path of headings for this section.",
    )

    content: str = Field(
        description="Content belonging to this section.",
    )
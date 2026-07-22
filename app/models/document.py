from uuid import uuid4

from pydantic import BaseModel, Field

from app.models.metadata import Metadata


class Document(BaseModel):
    """
    Original knowledge document before chunking.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique document identifier."
    )

    content: str = Field(
        description="Original document content."
    )

    metadata: Metadata
from uuid import uuid4
from pydantic import BaseModel, Field
from app.models.metadata import Metadata

class Chunk(BaseModel):
    """
    Smallest retrievable semantic unit.

    A Chunk is generated from a Document during the chunking stage.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique chunk identifier.",
    )

    document_id: str = Field(
        description="Parent document identifier.",
    )

    chunk_index: int = Field(
        description="Chunk order within the original document.",
    )

    content: str = Field(
        description="Chunk text content.",
    )

    metadata: Metadata

    start_offset: int = Field(
        description="Start character offset in the original document.",
    )

    end_offset: int = Field(
        description="End character offset in the original document.",
    )

    token_count: int = Field(
        default=0,
        description="Estimated number of tokens.",
    )
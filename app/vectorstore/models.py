
from pydantic import BaseModel, ConfigDict, Field

from app.models.chunk import Chunk


class VectorSearchResult(BaseModel):
    """A retrieved chunk and its similarity score."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    chunk: Chunk
    score: float = Field(
        description="Similarity score; higher means more similar."
    )

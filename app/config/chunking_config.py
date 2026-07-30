from pydantic import BaseModel


class ChunkingConfig(BaseModel):
    """
    Configuration for chunking strategies.
    """

    chunk_size: int = 500

    chunk_overlap: int = 50
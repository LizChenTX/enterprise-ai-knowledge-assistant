from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, model_validator



class ChunkConfig(BaseModel):
    chunk_size: int = Field(
        default=500,
        gt=0,
    )

    chunk_overlap: int = Field(
        default=0,
        ge=0,
    )

    @model_validator(mode="after")
    def validate_overlap(self) -> "ChunkConfig":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        return self
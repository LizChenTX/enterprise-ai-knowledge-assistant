
from app.embedding.base import EmbeddingProvider
from app.embedding.models import validate_embeddings


class MockEmbeddingProvider(EmbeddingProvider):
    """Deterministic embedding provider for tests and local development."""

    def __init__(self, dimensions: int = 8) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")

        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("text must not be empty")

        value = float(len(text) % 10) / 10
        vector = [value] * self.dimensions

        validate_embeddings([vector], expected_count=1)
        return vector

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = [self.embed(text) for text in texts]

        return validate_embeddings(
            embeddings,
            expected_count=len(texts),
        )

from app.embedding.base import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    """Deterministic embedding provider for tests and local development."""

    def __init__(self, dimensions: int = 8) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")

        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        """Return a deterministic, non-semantic vector for one text."""
        if not text.strip():
            raise ValueError("text must not be empty")

        # Intentionally simple: this is test data, not a real embedding.
        value = float(len(text) % 10) / 10
        return [value] * self.dimensions

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts using the same behavior as embed()."""
        return [self.embed(text) for text in texts]
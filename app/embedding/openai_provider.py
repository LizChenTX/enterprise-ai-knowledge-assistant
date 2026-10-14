
import os

from openai import OpenAI

from app.embedding.base import EmbeddingProvider
from app.embedding.models import validate_embeddings


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """Generate semantic embeddings using the OpenAI API."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: str | None = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not resolved_api_key:
            raise ValueError("OPENAI_API_KEY is required")

        self.model = model
        self.client = OpenAI(api_key=resolved_api_key)
        self.dimensions: int | None = None

    def embed(self, text: str) -> list[float]:
        embeddings = self.embed_batch([text])
        return embeddings[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("text must not be empty")

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        # Preserve the original input order explicitly.
        items = sorted(response.data, key=lambda item: item.index)
        embeddings = [item.embedding for item in items]

        validate_embeddings(
            embeddings,
            expected_count=len(texts),
        )

        current_dimensions = len(embeddings[0])
        if self.dimensions is None:
            self.dimensions = current_dimensions
        elif current_dimensions != self.dimensions:
            raise ValueError(
                f"Embedding dimension changed from {self.dimensions} "
                f"to {current_dimensions}"
            )

        return embeddings

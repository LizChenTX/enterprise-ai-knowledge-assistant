
import pytest

from app.embedding.base import EmbeddingProvider


def test_embedding_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        EmbeddingProvider()


def test_embedding_provider_requires_both_methods():
    class IncompleteProvider(EmbeddingProvider):
        def embed(self, text: str) -> list[float]:
            return [0.1, 0.2, 0.3]

    with pytest.raises(TypeError):
        IncompleteProvider()
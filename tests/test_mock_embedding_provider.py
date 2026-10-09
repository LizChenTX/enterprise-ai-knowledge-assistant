
import pytest

from app.embedding.mock_provider import MockEmbeddingProvider


def test_embed_returns_vector_with_configured_dimensions():
    provider = MockEmbeddingProvider(dimensions=4)

    vector = provider.embed("hello")

    assert len(vector) == 4
    assert vector == [0.5, 0.5, 0.5, 0.5]


def test_embed_is_deterministic():
    provider = MockEmbeddingProvider()

    assert provider.embed("hello") == provider.embed("hello")


def test_embed_batch_returns_one_vector_per_text():
    provider = MockEmbeddingProvider(dimensions=3)

    vectors = provider.embed_batch(["hello", "hi"])

    assert len(vectors) == 2
    assert vectors[0] == [0.5, 0.5, 0.5]
    assert vectors[1] == [0.2, 0.2, 0.2]


def test_embed_rejects_empty_text():
    provider = MockEmbeddingProvider()

    with pytest.raises(ValueError, match="text must not be empty"):
        provider.embed("   ")


def test_provider_rejects_invalid_dimensions():
    with pytest.raises(ValueError, match="dimensions must be positive"):
        MockEmbeddingProvider(dimensions=0)
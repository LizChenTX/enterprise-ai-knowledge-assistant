
from unittest.mock import MagicMock

import pytest

from app.embedding.openai_provider import OpenAIEmbeddingProvider


def test_provider_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        OpenAIEmbeddingProvider()


def test_embed_batch_preserves_input_order():
    provider = OpenAIEmbeddingProvider(api_key="test-key")
    provider.client = MagicMock()

    # Deliberately return vectors out of order.
    provider.client.embeddings.create.return_value.data = [
        MagicMock(index=1, embedding=[0.3, 0.4]),
        MagicMock(index=0, embedding=[0.1, 0.2]),
    ]

    result = provider.embed_batch(["first", "second"])

    assert result == [[0.1, 0.2], [0.3, 0.4]]
    provider.client.embeddings.create.assert_called_once()


def test_embed_rejects_empty_text():
    provider = OpenAIEmbeddingProvider(api_key="test-key")

    with pytest.raises(ValueError, match="text must not be empty"):
        provider.embed("   ")

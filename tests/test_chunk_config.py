import pytest

from app.config.chunking_config import ChunkConfig


def test_default_chunk_config():
    config = ChunkConfig()

    assert config.chunk_size == 500
    assert config.chunk_overlap == 0


def test_custom_chunk_config():
    config = ChunkConfig(
        chunk_size=100,
        chunk_overlap=20,
    )

    assert config.chunk_size == 100
    assert config.chunk_overlap == 20


def test_overlap_cannot_equal_chunk_size():
    with pytest.raises(ValueError):
        ChunkConfig(
            chunk_size=100,
            chunk_overlap=100,
        )


def test_overlap_cannot_exceed_chunk_size():
    with pytest.raises(ValueError):
        ChunkConfig(
            chunk_size=100,
            chunk_overlap=200,
        )
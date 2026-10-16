
import pytest

from app.models.chunk import Chunk
from app.vectorstore.numpy_store import NumpyVectorStore


def make_chunk(content: str, chunk_index: int) -> Chunk:
    return Chunk.model_construct(
        document_id="test-document",
        chunk_index=chunk_index,
        content=content,
        section_path=["Testing"],
        metadata={},
        start_offset=0,
        end_offset=len(content),
    )


def test_add_and_search_returns_most_similar_chunks_first():
    store = NumpyVectorStore()

    chunks = [
        make_chunk("Python testing", 0),
        make_chunk("Database architecture", 1),
        make_chunk("API test automation", 2),
    ]

    embeddings = [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.8, 0.2],
    ]

    store.add(chunks, embeddings)

    results = store.search([1.0, 0.0], top_k=2)

    assert len(results) == 2
    assert results[0].chunk.content == "Python testing"
    assert results[1].chunk.content == "API test automation"
    assert results[0].score == pytest.approx(1.0)
    assert results[1].score == pytest.approx(0.8 / (0.8**2 + 0.2**2) ** 0.5)


def test_search_returns_empty_list_for_empty_store():
    store = NumpyVectorStore()

    assert store.search([1.0, 0.0]) == []


def test_add_supports_multiple_batches():
    store = NumpyVectorStore()

    store.add(
        [make_chunk("First", 0)],
        [[1.0, 0.0]],
    )
    store.add(
        [make_chunk("Second", 1)],
        [[0.0, 1.0]],
    )

    assert store.size == 2

    results = store.search([0.0, 1.0], top_k=1)

    assert results[0].chunk.content == "Second"


def test_add_rejects_mismatched_counts():
    store = NumpyVectorStore()

    with pytest.raises(ValueError, match="count mismatch"):
        store.add([make_chunk("First", 0)], [])


def test_add_rejects_inconsistent_dimensions():
    store = NumpyVectorStore()

    with pytest.raises(ValueError, match="dimensions"):
        store.add(
            [
                make_chunk("First", 0),
                make_chunk("Second", 1),
            ],
            [[1.0, 0.0], [1.0, 0.0, 0.0]],
        )


def test_add_rejects_dimension_change_between_batches():
    store = NumpyVectorStore()
    store.add([make_chunk("First", 0)], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="dimension mismatch"):
        store.add(
            [make_chunk("Second", 1)],
            [[1.0, 0.0, 0.0]],
        )


def test_search_rejects_query_dimension_mismatch():
    store = NumpyVectorStore()
    store.add([make_chunk("First", 0)], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="Query embedding dimension mismatch"):
        store.search([1.0, 0.0, 0.0])


def test_search_rejects_zero_query_vector():
    store = NumpyVectorStore()
    store.add([make_chunk("First", 0)], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="zero vector"):
        store.search([0.0, 0.0])


def test_search_rejects_non_positive_top_k():
    store = NumpyVectorStore()

    with pytest.raises(ValueError, match="top_k must be positive"):
        store.search([1.0, 0.0], top_k=0)


def test_failed_add_does_not_change_store():
    store = NumpyVectorStore()
    store.add([make_chunk("First", 0)], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="dimension mismatch"):
        store.add(
            [make_chunk("Invalid", 1)],
            [[1.0, 0.0, 0.0]],
        )

    assert store.size == 1
    assert store.search([1.0, 0.0])[0].chunk.content == "First"

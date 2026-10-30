
import math

import pytest

from app.models.chunk import Chunk
from app.models.enums import DocumentSource, DocumentType
from app.models.metadata import Metadata
from app.vectorstore.faiss_store import FaissVectorStore


def make_chunk(content: str, chunk_index: int = 0) -> Chunk:
    return Chunk(
        document_id="doc-1",
        chunk_index=chunk_index,
        content=content,
        section_path=["Test"],
        metadata=Metadata(
            title="test document",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.ARCHITECTURE,
        ),
        start_offset=chunk_index * 10,
        end_offset=chunk_index * 10 + len(content),
    )


def test_empty_store_has_zero_size():
    store = FaissVectorStore()

    assert store.size == 0
    assert store.search([1.0, 0.0]) == []


def test_add_vectors_updates_size():
    store = FaissVectorStore()
    chunks = [make_chunk("A", 0), make_chunk("B", 1)]
    embeddings = [[1.0, 0.0], [0.0, 1.0]]

    store.add(chunks, embeddings)

    assert store.size == 2


def test_search_returns_chunks_by_cosine_similarity():
    store = FaissVectorStore()
    chunks = [
        make_chunk("horizontal", 0),
        make_chunk("diagonal", 1),
        make_chunk("vertical", 2),
    ]
    embeddings = [
        [1.0, 0.0],
        [0.70710678, 0.70710678],
        [0.0, 1.0],
    ]

    store.add(chunks, embeddings)
    results = store.search([1.0, 0.0], top_k=3)

    assert [result.chunk.content for result in results] == [
        "horizontal",
        "diagonal",
        "vertical",
    ]
    assert results[0].score == pytest.approx(1.0)
    assert results[1].score == pytest.approx(0.70710678, abs=1e-6)
    assert results[2].score == pytest.approx(0.0, abs=1e-6)


def test_search_returns_correct_chunk_for_each_vector():
    store = FaissVectorStore()
    first = make_chunk("first", 0)
    second = make_chunk("second", 1)

    store.add(
        [first, second],
        [[0.0, 1.0], [1.0, 0.0]],
    )

    results = store.search([1.0, 0.0], top_k=1)

    assert len(results) == 1
    assert results[0].chunk.id == second.id


def test_top_k_larger_than_store_size_returns_all_results():
    store = FaissVectorStore()
    chunks = [make_chunk("A", 0), make_chunk("B", 1)]

    store.add(chunks, [[1.0, 0.0], [0.0, 1.0]])

    assert len(store.search([1.0, 0.0], top_k=10)) == 2


def test_top_k_must_be_positive():
    store = FaissVectorStore()

    with pytest.raises(ValueError, match="top_k must be positive"):
        store.search([1.0, 0.0], top_k=0)


def test_add_rejects_mismatched_chunk_and_embedding_counts():
    store = FaissVectorStore()

    with pytest.raises(ValueError, match="count mismatch"):
        store.add([make_chunk("A")], [])


def test_add_rejects_inconsistent_dimensions_across_calls():
    store = FaissVectorStore()
    store.add([make_chunk("A")], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="dimension mismatch"):
        store.add([make_chunk("B", 1)], [[1.0, 0.0, 0.0]])

    assert store.size == 1


def test_add_rejects_zero_vectors():
    store = FaissVectorStore()

    with pytest.raises(ValueError, match="zero vectors"):
        store.add([make_chunk("A")], [[0.0, 0.0]])


def test_search_rejects_zero_query_vector():
    store = FaissVectorStore()
    store.add([make_chunk("A")], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="zero vector"):
        store.search([0.0, 0.0])


def test_search_rejects_wrong_query_dimensions():
    store = FaissVectorStore()
    store.add([make_chunk("A")], [[1.0, 0.0]])

    with pytest.raises(ValueError, match="dimension mismatch"):
        store.search([1.0, 0.0, 0.0])


def test_add_rejects_non_finite_values():
    store = FaissVectorStore()

    with pytest.raises(ValueError, match="non-finite"):
        store.add([make_chunk("A")], [[math.nan, 1.0]])


def test_adding_vectors_multiple_times_preserves_existing_results():
    store = FaissVectorStore()
    first = make_chunk("first", 0)
    second = make_chunk("second", 1)

    store.add([first], [[1.0, 0.0]])
    store.add([second], [[0.0, 1.0]])

    results = store.search([0.0, 1.0], top_k=2)

    assert store.size == 2
    assert results[0].chunk.id == second.id
    assert results[1].chunk.id == first.id


import pytest

from app.embedding.mock_provider import MockEmbeddingProvider
from app.models.chunk import Chunk
from app.models.metadata import DocumentSource, DocumentType, Metadata
from app.retrieval.retriever import Retriever
from app.vectorstore.faiss_store import FaissVectorStore


def make_chunk(content: str, index: int = 0) -> Chunk:
    return Chunk(
        document_id="test-document",
        chunk_index=index,
        content=content,
        section_path=["Testing"],
        metadata=Metadata(
            title="Test document",
            source=DocumentSource.MARKDOWN,
            document_type=DocumentType.TUTORIAL,
        ),
        start_offset=0,
        end_offset=len(content),
    )


def make_retriever() -> Retriever:
    embedding_provider = MockEmbeddingProvider(dimensions=8)
    vector_store = FaissVectorStore()

    chunks = [
        make_chunk("A short text.", index=0),
        make_chunk("A longer example text.", index=1),
    ]
    embeddings = embedding_provider.embed_batch(
        [chunk.content for chunk in chunks]
    )
    vector_store.add(chunks, embeddings)

    return Retriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )


def test_retrieve_returns_search_results():
    retriever = make_retriever()

    results = retriever.retrieve("Find a short text")

    assert len(results) > 0
    assert all(result.chunk is not None for result in results)
    assert all(isinstance(result.score, float) for result in results)


def test_retrieve_respects_top_k():
    retriever = make_retriever()

    results = retriever.retrieve("Find a short text", top_k=1)

    assert len(results) == 1


@pytest.mark.parametrize("query", ["", " ", "\t", "\n"])
def test_retrieve_rejects_empty_query(query):
    retriever = make_retriever()

    with pytest.raises(ValueError, match="query must not be empty"):
        retriever.retrieve(query)


@pytest.mark.parametrize("top_k", [0, -1])
def test_retrieve_rejects_non_positive_top_k(top_k):
    retriever = make_retriever()

    with pytest.raises(ValueError, match="top_k must be positive"):
        retriever.retrieve("Find a short text", top_k=top_k)


def test_retrieve_returns_empty_list_when_store_is_empty():
    retriever = Retriever(
        embedding_provider=MockEmbeddingProvider(dimensions=8),
        vector_store=FaissVectorStore(),
    )

    results = retriever.retrieve("Find a document")

    assert results == []

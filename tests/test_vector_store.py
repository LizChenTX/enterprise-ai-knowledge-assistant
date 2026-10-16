
import pytest

from app.vectorstore.base import VectorStore


def test_vector_store_is_abstract():
    with pytest.raises(TypeError):
        VectorStore()


def test_vector_store_requires_add_and_search():
    class IncompleteVectorStore(VectorStore):
        def add(self, chunks, embeddings):
            pass

    with pytest.raises(TypeError):
        IncompleteVectorStore()

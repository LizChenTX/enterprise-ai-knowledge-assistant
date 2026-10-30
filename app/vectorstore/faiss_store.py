

import faiss
import numpy as np

from app.embedding.models import validate_embeddings
from app.models.chunk import Chunk
from app.vectorstore.base import VectorStore
from app.vectorstore.models import VectorSearchResult


class FaissVectorStore(VectorStore):
    """In-memory vector store using FAISS inner-product search.

    All vectors are normalized before insertion and querying, so inner
    product scores are equivalent to cosine similarity.
    """

    def __init__(self) -> None:
        self._index: faiss.IndexFlatIP | None = None
        self._chunks: list[Chunk] = []
        self._dimensions: int | None = None

    @property
    def size(self) -> int:
        """Return the number of stored vectors."""
        return len(self._chunks)

    def add(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Chunks and embeddings count mismatch: "
                f"{len(chunks)} chunks, {len(embeddings)} embeddings"
            )

        if not chunks:
            return

        validate_embeddings(
            embeddings,
            expected_count=len(chunks),
        )

        dimensions = len(embeddings[0])

        if (
            self._dimensions is not None
            and dimensions != self._dimensions
        ):
            raise ValueError(
                f"Embedding dimension mismatch: expected "
                f"{self._dimensions}, got {dimensions}"
            )

        vectors = np.asarray(embeddings, dtype=np.float32)

        # Float conversion can overflow even when the original values
        # are finite, so validate again after conversion.
        if not np.isfinite(vectors).all():
            raise ValueError(
                "Embeddings contain invalid values after conversion"
            )

        norms = np.linalg.norm(vectors, axis=1)

        if not np.isfinite(norms).all():
            raise ValueError("Embedding vector norms must be finite")

        if np.any(norms == 0):
            raise ValueError("Embedding vectors must not be zero vectors")

        normalized_vectors = vectors / norms[:, np.newaxis]

        # Build the index locally so validation errors cannot partially
        # mutate the existing store.
        if self._index is None:
            index = faiss.IndexFlatIP(dimensions)
        else:
            index = self._index

        index.add(np.ascontiguousarray(normalized_vectors))

        self._index = index
        self._dimensions = dimensions
        self._chunks.extend(chunks)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        if self._index is None or self.size == 0:
            return []

        validate_embeddings(
            [query_embedding],
            expected_count=1,
        )

        if len(query_embedding) != self._dimensions:
            raise ValueError(
                f"Query embedding dimension mismatch: expected "
                f"{self._dimensions}, got {len(query_embedding)}"
            )

        query = np.asarray(query_embedding, dtype=np.float32)

        if not np.isfinite(query).all():
            raise ValueError(
                "Query embedding contains invalid values after conversion"
            )

        query_norm = np.linalg.norm(query)

        if not np.isfinite(query_norm):
            raise ValueError("Query vector norm must be finite")

        if query_norm == 0:
            raise ValueError("Query embedding must not be a zero vector")

        normalized_query = query / query_norm
        normalized_query = np.ascontiguousarray(
            normalized_query.reshape(1, -1)
        )

        scores, indices = self._index.search(
            normalized_query,
            min(top_k, self.size),
        )

        return [
            VectorSearchResult(
                chunk=self._chunks[int(index)],
                score=float(score),
            )
            for score, index in zip(scores[0], indices[0])
            if index >= 0
        ]

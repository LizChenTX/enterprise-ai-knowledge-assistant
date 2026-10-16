
import numpy as np

from app.embedding.models import validate_embeddings
from app.models.chunk import Chunk
from app.vectorstore.base import VectorStore
from app.vectorstore.models import VectorSearchResult


class NumpyVectorStore(VectorStore):
    """In-memory vector store using NumPy cosine similarity."""

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._vectors: np.ndarray | None = None
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

        vectors = np.asarray(embeddings, dtype=np.float64)

        if not np.isfinite(vectors).all():
            raise ValueError(
                "Embeddings contain invalid values after conversion"
            )

        norms = np.linalg.norm(vectors, axis=1)

        if not np.isfinite(norms).all():
            raise ValueError("Embedding vector norms must be finite")

        if np.any(norms == 0):
            raise ValueError("Embedding vectors must not be zero vectors")

        # Normalize each vector to unit length.
        normalized_vectors = vectors / norms[:, np.newaxis]

        # Commit the update only after validation succeeds.
        if self._vectors is None:
            self._vectors = normalized_vectors
            self._dimensions = dimensions
        else:
            self._vectors = np.concatenate(
                [self._vectors, normalized_vectors],
                axis=0,
            )

        self._chunks.extend(chunks)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        if self._vectors is None or self.size == 0:
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

        query = np.asarray(query_embedding, dtype=np.float64)

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

        # All stored vectors are normalized, so dot product is cosine similarity.
        scores = self._vectors @ normalized_query

        # Stable sorting makes equal-score results deterministic.
        ranked_indices = np.argsort(-scores, kind="stable")
        top_indices = ranked_indices[: min(top_k, self.size)]

        return [
            VectorSearchResult(
                chunk=self._chunks[int(index)],
                score=float(scores[index]),
            )
            for index in top_indices
        ]

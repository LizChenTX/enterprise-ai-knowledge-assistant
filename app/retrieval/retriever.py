
from app.embedding.base import EmbeddingProvider
from app.vectorstore.base import VectorStore
from app.vectorstore.models import VectorSearchResult


class Retriever:
    """Retrieve relevant chunks for a natural-language query."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        """Embed a query and retrieve the most similar chunks."""
        if not query.strip():
            raise ValueError("query must not be empty")

        if top_k <= 0:
            raise ValueError("top_k must be positive")

        query_embedding = self.embedding_provider.embed(query)

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

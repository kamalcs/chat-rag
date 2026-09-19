from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


class RetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        score_threshold: float | None = None,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.score_threshold = score_threshold

    def retrieve(self, query: str, limit: int = 5):
        if not query.strip():
            return []

        query_vector = self.embedding_service.embed(query)

        results = self.vector_store.search(vector=query_vector, limit=limit)

        if self.score_threshold is not None:
            results = [result for result in results if result.score >= self.score_threshold]

        return results

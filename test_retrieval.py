from app.core.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.retrieval_service import RetrievalService

embedding_service = EmbeddingService(model_name=settings.embedding_model)

vector_store = VectorStore(
    path=settings.qdrant_path,
    collection_name=settings.qdrant_collection,
    vector_size=settings.embedding_dimension,
)

retrieval_service = RetrievalService(
    embedding_service=embedding_service, vector_store=vector_store
)


question = "What is Redis used for?"

results = retrieval_service.retrieve(query=question, limit=3)


print(f"Question: {question}")
print("=" * 60)

for index, result in enumerate(results, start=1):

    print(f"\nResult #{index}")
    print(f"Score: {result.score}")

    payload = result.payload

    print(f"File: {payload['file_name']}")
    print(f"Chunk: {payload['chunk_index']}")
    print("Text:")
    print(payload["text"])


vector_store.close()

from app.core.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

question = "What is Redis used for?"


# Create embedding service
embedding_service = EmbeddingService(model_name=settings.embedding_model)


# Convert question to vector
question_vector = embedding_service.embed(question)

print(f"Question: {question}")
print(f"Vector dimension: {len(question_vector)}")


# Connect to Qdrant
vector_store = VectorStore(
    path=settings.qdrant_path,
    collection_name=settings.qdrant_collection,
    vector_size=settings.embedding_dimension,
)


# Search
results = vector_store.search(vector=question_vector, limit=3)


print()
print(f"Results found: {len(results)}")
print("=" * 60)


for index, result in enumerate(results, start=1):

    print(f"\nResult #{index}")
    print(f"Score: {result.score}")

    payload = result.payload

    print(f"File: {payload['file_name']}")
    print(f"Chunk: {payload['chunk_index']}")
    print(f"Text:")
    print(payload["text"])


vector_store.close()

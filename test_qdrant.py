from app.core.config import settings
from app.services.vector_store import VectorStore

vector_store = VectorStore(
    path=settings.qdrant_path,
    collection_name=settings.qdrant_collection,
    vector_size=settings.embedding_dimension,
)

print("Qdrant initialized successfully.")
print(f"Collection: {settings.qdrant_collection}")

vector_store.close()

print("Qdrant closed successfully.")

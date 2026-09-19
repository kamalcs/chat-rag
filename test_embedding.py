from app.services.embedding_service import EmbeddingService

service = EmbeddingService()


text = "Redis is used for caching."

vector = service.embed(text)


print(f"Vector dimensions: {len(vector)}")
print(f"First 10 values: {vector[:10]}")

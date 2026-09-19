from pathlib import Path

from app.core.config import settings
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.text_cleaner import TextCleaner
from app.ingestion.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

FILE_PATH = "data/documents/test.txt"


# 1. Load document
loader = DocumentLoader()

text = loader.load(FILE_PATH)

print("Document loaded.")
print(f"Characters: {len(text)}")


# 2. Clean document
cleaner = TextCleaner()

cleaned_text = cleaner.clean(text)

print("Document cleaned.")
print(f"Characters after cleaning: {len(cleaned_text)}")


# 3. Create chunks
chunker = TextChunker(chunk_size=2000, chunk_overlap=200)

file_name = Path(FILE_PATH).name

chunks = chunker.split(
    text=cleaned_text, document_id="test-document-001", file_name=file_name
)

print(f"Chunks created: {len(chunks)}")


# 4. Create embeddings
embedding_service = EmbeddingService(model_name=settings.embedding_model)

texts = [chunk.text for chunk in chunks]

vectors = embedding_service.embed_many(texts)

print(f"Embeddings created: {len(vectors)}")
print(f"Vector dimension: {len(vectors[0])}")


# 5. Store in Qdrant
vector_store = VectorStore(
    path=settings.qdrant_path,
    collection_name=settings.qdrant_collection,
    vector_size=settings.embedding_dimension,
)

vector_store.add_chunks(chunks=chunks, vectors=vectors)

print("Chunks stored in Qdrant.")
print(f"Collection: {settings.qdrant_collection}")


# 6. Close Qdrant
vector_store.close()

print("Qdrant closed.")

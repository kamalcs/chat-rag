from app.ingestion.document_loader import DocumentLoader
from app.ingestion.text_cleaner import TextCleaner
from app.ingestion.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService

loader = DocumentLoader()
cleaner = TextCleaner()

chunker = TextChunker(chunk_size=200, chunk_overlap=50)

embedding_service = EmbeddingService()


file_path = "data/documents/test.txt"

text = loader.load(file_path)

clean_text = cleaner.clean(text)

chunks = chunker.split(text=clean_text, document_id="doc-001", file_name="test.txt")


texts = [chunk.text for chunk in chunks]

vectors = embedding_service.embed_many(texts)


print(f"Chunks: {len(chunks)}")
print(f"Vectors: {len(vectors)}")

for index, vector in enumerate(vectors):

    print()
    print(f"Chunk: {index}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")

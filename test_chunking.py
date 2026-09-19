from app.ingestion.document_loader import DocumentLoader
from app.ingestion.text_cleaner import TextCleaner
from app.ingestion.text_chunker import TextChunker

loader = DocumentLoader()
cleaner = TextCleaner()

chunker = TextChunker(chunk_size=200, chunk_overlap=50)


file_path = "data/documents/test.txt"

text = loader.load(file_path)

clean_text = cleaner.clean(text)

chunks = chunker.split(text=clean_text, document_id="doc-001", file_name="test.txt")


print(f"Number of chunks: {len(chunks)}")

for chunk in chunks:

    print()
    print(f"--- Chunk {chunk.chunk_index} ---")
    print(f"Document: {chunk.document_id}")
    print(f"File: {chunk.file_name}")
    print(f"Page: {chunk.page_number}")
    print(chunk.text)

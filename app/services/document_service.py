import uuid

from app.ingestion.document_loader import DocumentLoader

from app.ingestion.text_cleaner import TextCleaner

from app.ingestion.text_chunker import TextChunker

from app.services.embedding_service import EmbeddingService

from app.services.vector_store import VectorStore


class DocumentService:

    def __init__(
        self,
        document_loader: DocumentLoader,
        text_cleaner: TextCleaner,
        text_chunker: TextChunker,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):

        self.document_loader = document_loader

        self.text_cleaner = text_cleaner

        self.text_chunker = text_chunker

        self.embedding_service = embedding_service

        self.vector_store = vector_store

    def ingest(self, file_path: str, original_file_name: str) -> dict:

        # Generate a unique ID
        # for this document.
        document_id = str(uuid.uuid4())

        # 1. Extract text from file.
        text = self.document_loader.load(file_path)

        # 2. Clean extracted text.
        cleaned_text = self.text_cleaner.clean(text)

        if not cleaned_text:

            raise ValueError("No text could be extracted " "from the document.")

        # 3. Split document into chunks.
        chunks = self.text_chunker.split(
            text=cleaned_text, document_id=document_id, file_name=original_file_name
        )

        if not chunks:

            raise ValueError("No chunks could be created " "from the document.")

        # 4. Get text from every chunk.
        texts = [chunk.text for chunk in chunks]

        # 5. Generate embeddings.
        vectors = self.embedding_service.embed_many(texts)

        # 6. Store chunks + embeddings
        # inside Qdrant.
        self.vector_store.add_chunks(chunks=chunks, vectors=vectors)

        return {
            "document_id": document_id,
            "file_name": original_file_name,
            "chunks": len(chunks),
        }

from app.models.document import DocumentChunk


class TextChunker:

    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str, document_id: str, file_name: str) -> list[DocumentChunk]:

        if not text:
            return []

        chunks = []

        start = 0
        chunk_index = 0

        text_length = len(text)

        while start < text_length:

            end = start + self.chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append(
                    DocumentChunk(
                        document_id=document_id,
                        file_name=file_name,
                        chunk_index=chunk_index,
                        text=chunk_text,
                    )
                )

                chunk_index += 1

            start = end - self.chunk_overlap

        return chunks

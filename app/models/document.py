from pydantic import BaseModel


class DocumentChunk(BaseModel):
    document_id: str
    file_name: str
    chunk_index: int
    text: str
    page_number: int | None = None

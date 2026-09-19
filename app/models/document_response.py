from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    file_name: str
    chunks: int

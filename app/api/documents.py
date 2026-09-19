from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import settings

from app.core.dependencies import get_document_service

from app.models.document_response import DocumentUploadResponse

from app.services.document_service import DocumentService

router = APIRouter(prefix="/api/documents", tags=["Documents"])


ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
):

    original_file_name = file.filename

    if not original_file_name:

        raise HTTPException(status_code=400, detail="File name is required.")

    extension = Path(original_file_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=("Unsupported file type. " "Allowed types: " ".txt, .pdf, .docx"),
        )

    upload_directory = Path(settings.document_upload_path)

    upload_directory.mkdir(parents=True, exist_ok=True)

    stored_file_name = f"{uuid.uuid4()}{extension}"

    file_path = upload_directory / stored_file_name

    try:

        # Save uploaded file.
        with file_path.open("wb") as buffer:

            shutil.copyfileobj(file.file, buffer)

        # Process document.
        result = document_service.ingest(
            file_path=str(file_path), original_file_name=(original_file_name)
        )

        return DocumentUploadResponse(
            document_id=(result["document_id"]),
            file_name=(result["file_name"]),
            chunks=result["chunks"],
        )

    except ValueError as ex:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(status_code=400, detail=str(ex))

    except Exception:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(status_code=500, detail=("Failed to process document."))

    finally:

        await file.close()

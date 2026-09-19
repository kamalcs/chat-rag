from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.dependencies import get_rag_service
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask(request: ChatRequest, rag_service: RAGService = Depends(get_rag_service)):

    answer = rag_service.ask(question=request.question, limit=settings.retrieval_limit)

    return ChatResponse(question=request.question, answer=answer)

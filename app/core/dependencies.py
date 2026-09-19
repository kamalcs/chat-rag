from app.core.config import settings

from app.ingestion.document_loader import DocumentLoader

from app.ingestion.text_cleaner import TextCleaner

from app.ingestion.text_chunker import TextChunker

from app.services.embedding_service import EmbeddingService

from app.services.vector_store import VectorStore

from app.services.retrieval_service import RetrievalService

from app.services.prompt_service import PromptService

from app.services.llm_service import LLMService

from app.services.rag_service import RAGService

from app.services.document_service import DocumentService

# --------------------------------------------------
# Embedding
# --------------------------------------------------

embedding_service = EmbeddingService(model_name=settings.embedding_model)


# --------------------------------------------------
# Qdrant
# --------------------------------------------------

vector_store = VectorStore(
    path=settings.qdrant_path,
    collection_name=(settings.qdrant_collection),
    vector_size=(settings.embedding_dimension),
)


# --------------------------------------------------
# Document ingestion components
# --------------------------------------------------

document_loader = DocumentLoader()

text_cleaner = TextCleaner()

text_chunker = TextChunker(chunk_size=2000, chunk_overlap=200)


# --------------------------------------------------
# Document Service
# --------------------------------------------------

document_service = DocumentService(
    document_loader=document_loader,
    text_cleaner=text_cleaner,
    text_chunker=text_chunker,
    embedding_service=embedding_service,
    vector_store=vector_store,
)


# --------------------------------------------------
# Retrieval Service
# --------------------------------------------------

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store,
    score_threshold=(settings.retrieval_score_threshold),
)


# --------------------------------------------------
# Prompt Service
# --------------------------------------------------

prompt_service = PromptService()


# --------------------------------------------------
# Ollama
# --------------------------------------------------

llm_service = LLMService(host=settings.ollama_host, model=settings.ollama_model)


# --------------------------------------------------
# RAG Service
# --------------------------------------------------

rag_service = RAGService(
    retrieval_service=retrieval_service,
    prompt_service=prompt_service,
    llm_service=llm_service,
)


# --------------------------------------------------
# FastAPI dependencies
# --------------------------------------------------


def get_rag_service() -> RAGService:

    return rag_service


def get_document_service() -> DocumentService:

    return document_service

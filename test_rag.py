from app.core.config import settings

from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.retrieval_service import RetrievalService
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService

embedding_service = EmbeddingService(model_name=settings.embedding_model)


vector_store = VectorStore(
    path=settings.qdrant_path,
    collection_name=settings.qdrant_collection,
    vector_size=settings.embedding_dimension,
)


try:
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        score_threshold=settings.retrieval_score_threshold,
    )
    prompt_service = PromptService()
    llm_service = LLMService(host=settings.ollama_host, model=settings.ollama_model)
    rag_service = RAGService(
        retrieval_service=retrieval_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )
    questions = ["What is Redis used for?", "Who invented Python?"]

    for question in questions:

        answer = rag_service.ask(question=question, limit=settings.retrieval_limit)

        print()
        print("=" * 60)

        print("Question:")
        print(question)

        print()

        print("Answer:")
        print(answer)

finally:

    vector_store.close()

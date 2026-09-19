from app.services.retrieval_service import RetrievalService
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService


class RAGService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_service: PromptService,
        llm_service: LLMService,
    ):
        self.retrieval_service = retrieval_service
        self.prompt_service = prompt_service
        self.llm_service = llm_service

    def ask(self, question: str, limit: int = 3) -> str:

        results = self.retrieval_service.retrieve(query=question, limit=limit)

        if not results:
            return "I don't know based on the provided documents."

        contexts = [result.payload["text"] for result in results]

        prompt = self.prompt_service.build_rag_prompt(
            question=question, contexts=contexts
        )

        answer = self.llm_service.generate(prompt=prompt)

        return answer

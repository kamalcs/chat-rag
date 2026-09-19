from app.core.config import settings
from app.services.llm_service import LLMService

llm_service = LLMService(host=settings.ollama_host, model=settings.ollama_model)


answer = llm_service.generate("Say hello in one sentence.")


print(answer)

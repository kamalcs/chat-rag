from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Chat RAG"
    app_version: str = "0.1.0"
    debug: bool = False

    document_upload_path: str = "data/documents"

    qdrant_path: str = "data/qdrant"
    qdrant_collection: str = "chat_documents"

    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    retrieval_score_threshold: float = 0.40
    retrieval_limit: int = 3

    llm_provider: str = "ollama"

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()

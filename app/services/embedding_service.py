from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):

        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:

        if not text:
            return []

        vector = self.model.encode(text)

        return vector.tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:

        if not texts:
            return []

        vectors = self.model.encode(texts)

        return vectors.tolist()

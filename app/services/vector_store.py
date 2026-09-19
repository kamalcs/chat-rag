import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.models.document import DocumentChunk


class VectorStore:

    def __init__(self, path: str, collection_name: str, vector_size: int):

        self.collection_name = collection_name

        self.client = QdrantClient(path=path)

        self._create_collection(vector_size)

    def _create_collection(self, vector_size: int):

        collections = self.client.get_collections()

        collection_exists = any(
            collection.name == self.collection_name
            for collection in collections.collections
        )

        if not collection_exists:

            self.client.create_collection(
                collection_name=(self.collection_name),
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def add_chunks(self, chunks: list[DocumentChunk], vectors: list[list[float]]):

        if len(chunks) != len(vectors):

            raise ValueError(
                "The number of chunks must " "match the number of vectors."
            )

        points = []

        for chunk, vector in zip(chunks, vectors):

            point = PointStruct(
                id=str(uuid.uuid4()), vector=vector, payload=chunk.model_dump()
            )

            points.append(point)

        if points:

            self.client.upsert(collection_name=(self.collection_name), points=points)

    def search(self, vector: list[float], limit: int = 5):

        results = self.client.query_points(
            collection_name=(self.collection_name),
            query=vector,
            limit=limit,
            with_payload=True,
        )

        return results.points

    def close(self):

        self.client.close()

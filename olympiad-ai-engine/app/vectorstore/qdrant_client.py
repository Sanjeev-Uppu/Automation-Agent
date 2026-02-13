from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition, MatchValue

# Persistent storage
client = QdrantClient(path="qdrant_data")

def create_collection(name: str, vector_size: int = 384):
    client.recreate_collection(
        collection_name=name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )


def search_similar(collection_name: str, query_vector: list, chapter_name: str = None, limit: int = 3):

    search_filter = None

    if chapter_name:
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="chapter_name",
                    match=MatchValue(value=chapter_name)
                )
            ]
        )

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=search_filter,
        limit=limit
    )

    return [point.payload for point in results.points]

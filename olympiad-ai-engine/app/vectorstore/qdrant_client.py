import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    MatchValue
)

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def create_collection(collection_name: str, vector_size: int = 384):

    existing = [c.name for c in client.get_collections().collections]

    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    # Ensure payload indexes exist
    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name="chapter_name",
            field_schema="keyword"
        )
    except:
        pass

    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name="type",
            field_schema="keyword"
        )
    except:
        pass


def search_similar(
    collection_name: str,
    query_vector: list,
    chapter_name: str = None,
    limit: int = 3
):

    query_filter = None

    if chapter_name:
        query_filter = Filter(
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
        query_filter=query_filter,
        limit=limit
    )

    return [point.payload for point in results.points]

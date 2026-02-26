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

_client = None


def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            timeout=5  # VERY IMPORTANT (prevents hanging)
        )
    return _client


# --------------------------------------------------
# CREATE COLLECTION
# --------------------------------------------------

def create_collection(collection_name: str, vector_size: int = 384):

    client = get_client()

    existing = [c.name for c in client.get_collections().collections]

    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        client.create_payload_index(
            collection_name=collection_name,
            field_name="subject",
            field_schema="keyword"
        )

        client.create_payload_index(
            collection_name=collection_name,
            field_name="chapter_name",
            field_schema="keyword"
        )


# --------------------------------------------------
# SEARCH SIMILAR
# --------------------------------------------------

def search_similar(
    *,
    grade: int,
    subject: str,
    query_vector: list,
    chapter_name: str = None,
    limit: int = 3
):

    client = get_client()

    collection_name = f"olympiad_grade_{grade}"

    must_conditions = [
        FieldCondition(
            key="subject",
            match=MatchValue(value=subject.lower())
        )
    ]

    if chapter_name:
        must_conditions.append(
            FieldCondition(
                key="chapter_name",
                match=MatchValue(value=chapter_name.lower())
            )
        )

    query_filter = Filter(must=must_conditions)

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=query_filter,
        limit=limit
    )

    return [point.payload for point in results.points]
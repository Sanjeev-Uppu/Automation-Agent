import uuid
from app.services.gemini_pdf_loader import load_pdf
from app.services.chunking import split_into_concepts
from app.embeddings.embedder import generate_embedding
from app.vectorstore.qdrant_client import client, create_collection
from qdrant_client.models import PointStruct


def ingest_pdf(file_path: str, grade: int, subject: str, chapter_name: str):

    collection_name = f"olympiad_grade_{grade}"

    create_collection(collection_name)

    text = load_pdf(file_path)

    concepts = split_into_concepts(text)

    points = []

    for concept in concepts:
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=generate_embedding(concept),
                payload={
                    "grade": grade,
                    "subject": subject.lower(),
                    "chapter_name": chapter_name.lower(),
                    "content": concept,
                    "type": "concept"
                }
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    return {
        "status": "Ingestion Complete",
        "chunks": len(points)
    }
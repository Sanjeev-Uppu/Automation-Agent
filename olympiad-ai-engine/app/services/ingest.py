from app.services.pdf_loader import load_pdf
from app.services.chunking import split_into_concepts
from app.embeddings.embedder import generate_embedding
from app.vectorstore.qdrant_client import client, create_collection
from qdrant_client.models import PointStruct
import uuid

def ingest_pdf(file_path: str, grade: int, subject: str, chapter_name: str):

    collection_name = f"olympiad_{grade}_{subject}"
    create_collection(collection_name)

    text = load_pdf(file_path)
    concepts = split_into_concepts(text)

    points = []

    # Store concept chunks
    for concept in concepts:
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=generate_embedding(concept),
                payload={
                    "chapter_name": chapter_name,
                    "grade": grade,
                    "subject": subject,
                    "content": concept,
                    "type": "concept"
                }
            )
        )

    # Store FULL chapter
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=generate_embedding(text),
            payload={
                "chapter_name": chapter_name,
                "grade": grade,
                "subject": subject,
                "content": text,
                "type": "full_chapter"
                }
            )
        )

    client.upsert(collection_name=collection_name, points=points)

    return {"status": "Ingestion Complete", "chunks": len(points)}

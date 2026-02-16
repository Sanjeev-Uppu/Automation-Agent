from fastapi import APIRouter

from app.embeddings.embedder import generate_embedding
from app.vectorstore.qdrant_client import search_similar
from app.services.qa_engine import generate_answer
from app.models.request_models import AskRequest

router = APIRouter(prefix="/chat", tags=["Chat Engine"])


@router.post("/")
def chat(request: AskRequest):

    collection_name = f"olympiad_{request.grade}_{request.subject.strip()}"

    query_vector = generate_embedding(request.question)

    # ✅ FIXED CALL
    results = search_similar(
        collection_name=collection_name,
        query_vector=query_vector,
        chapter_name=request.chapter_name,
        limit=3
    )

    if not results:
        return {"answer": "Answer not found in lesson."}

    context = "\n\n".join([r["content"] for r in results])

    answer = generate_answer(context, request.question)

    return {"answer": answer}

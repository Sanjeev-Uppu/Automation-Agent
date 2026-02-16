from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware

import os
import uuid
from typing import List, Optional
from app.vectorstore.qdrant_client import client

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from app.models.request_models import AskRequest
from app.models.mock_models import MockRequest, SubmissionRequest

from app.embeddings.embedder import generate_embedding
from app.vectorstore.qdrant_client import search_similar



from app.services.qa_engine import generate_answer
from app.services.mock_engine import generate_mock_exam_llm
from app.services.deterministic_mock_engine import generate_mock_exam as generate_fallback_mock
from app.services.planner_engine import generate_llm_plan
from app.services.deterministic_planner import generate_fallback_plan
from app.services.pdf_exam_generator import generate_exam_pdf
from app.services.pdf_planner_generator import generate_planner_pdf
from app.services.ingest import ingest_pdf
from app.services.bulk_ingest import ingest_all_pdfs
from google.genai.errors import ClientError


# --------------------------------------------------
# 🚀 FASTAPI APP
# --------------------------------------------------

app = FastAPI(title="Olympiad Mastery AI Engine")

# --------------------------------------------------
# 🌍 CORS CONFIG
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# 📦 RESPONSE MODEL (Optional legacy support)
# --------------------------------------------------

class AskResponse(BaseModel):
    question: str
    answer_type: str
    count: Optional[int] = None
    data: Optional[List[str]] = None
    explanation: Optional[str] = None


# --------------------------------------------------
# 🏠 ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {"message": "Olympiad AI Engine Running Successfully"}


# --------------------------------------------------
# 📥 INGEST PDF
# --------------------------------------------------

@app.post("/ingest/")
def ingest():
    return ingest_pdf(
        file_path="data/pdfs/Animals.pdf",
        grade=5,
        subject="science",
        chapter_name="Animals"
    )


# --------------------------------------------------
# 💬 ASK ENDPOINT (Dynamic Chat + PDF)
# --------------------------------------------------

@app.post("/ask/")
def ask_question(request: AskRequest):

    user_query = request.question.lower()
    collection_name = f"olympiad_{request.grade}_{request.subject}"

    # --------------------------------------------------
    # 📄 QUESTION PAPER PDF REQUEST
    # --------------------------------------------------
    if "pdf" in user_query and "question paper" in user_query:

        results = search_similar(
            collection_name,
            generate_embedding(request.chapter_name),
            request.chapter_name,
            limit=5
        )

        if not results:
            return {"type": "text", "message": "Chapter content not found."}

        context_text = "\n\n".join([r["content"] for r in results])
        context_text = context_text[:4000]  # 🔥 Prevent token overflow

        mock_data = generate_mock_exam_llm(context_text, request.chapter_name)

        os.makedirs("generated_pdfs", exist_ok=True)
        filename = f"question_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join("generated_pdfs", filename)

        generate_exam_pdf(mock_data, file_path)

        return {
            "type": "pdf",
            "message": "Your question paper is ready.",
            "download_url": f"http://127.0.0.1:8002/download/{filename}"
        }

    # --------------------------------------------------
    # 🗓️ PLANNER PDF REQUEST
    # --------------------------------------------------
    if "planner" in user_query and "pdf" in user_query:

        try:
            plan_data = generate_llm_plan(7, request.chapter_name)
        except Exception:
            plan_data = generate_fallback_plan(7, request.chapter_name)

        os.makedirs("generated_pdfs", exist_ok=True)
        filename = f"planner_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join("generated_pdfs", filename)

        generate_planner_pdf(plan_data, file_path)

        return {
            "type": "pdf",
            "message": "Your study planner PDF is ready.",
            "download_url": f"http://127.0.0.1:8002/download/{filename}"
        }

    # --------------------------------------------------
    # 🔹 NORMAL QA FLOW
    # --------------------------------------------------

    query_vector = generate_embedding(request.question)

    results = search_similar(
        collection_name,
        query_vector,
        request.chapter_name,
        limit=3
    )

    if not results:
        return {"type": "text", "message": "Not available in the lesson."}

    context_text = "\n\n".join([r["content"] for r in results])
    context_text = context_text[:4000]  # 🔥 Prevent Gemini crash

    answer = generate_answer(context_text, request.question)

    return {
        "type": "text",
        "message": answer
    }


# --------------------------------------------------
# 📝 GENERATE MOCK EXAM
# --------------------------------------------------

@app.post("/generate-mock/")
def generate_mock(request: MockRequest):

    collection_name = f"olympiad_{request.grade}_{request.subject}"

    results = search_similar(
        collection_name,
        generate_embedding(request.chapter_name),
        request.chapter_name,
        limit=5
    )

    if not results:
        return {"error": "Chapter content not found."}

    context_text = "\n\n".join([r["content"] for r in results])
    context_text = context_text[:4000]

    try:
        mock_data = generate_mock_exam_llm(context_text, request.chapter_name)
        print("✅ LLM Mock Used")
        return mock_data

    except ClientError:
        print("⚠️ Gemini quota exceeded. Switching to fallback.")

    except Exception as e:
        print("⚠️ LLM failed. Using fallback engine.")
        print("Error:", str(e))

    fallback_mock = generate_fallback_mock(context_text, request.chapter_name)
    print("✅ Deterministic Mock Used")
    return fallback_mock


# --------------------------------------------------
# 🧾 SUBMIT MOCK
# --------------------------------------------------

@app.post("/submit-mock/")
def submit_mock(submission: SubmissionRequest):

    score = 0

    for q in submission.questions:
        if q.selected_answer == q.correct_answer:
            score += 1

    total = len(submission.questions)

    return {
        "total_questions": total,
        "correct": score,
        "percentage": round((score / total) * 100, 2)
    }


# --------------------------------------------------
# 🗓️ GENERATE STUDY PLAN
# --------------------------------------------------

@app.post("/generate-plan/")
def generate_plan(duration_days: int, chapter_name: str):

    try:
        plan_data = generate_llm_plan(duration_days, chapter_name)
        print("✅ LLM Plan Used")
        return plan_data

    except Exception as e:
        print("⚠️ LLM failed. Using fallback.")
        print("Error:", str(e))
        return generate_fallback_plan(duration_days, chapter_name)


# --------------------------------------------------
# 📥 FILE DOWNLOAD ENDPOINT
# --------------------------------------------------

@app.get("/download/{filename}")
def download_file(filename: str):

    file_path = os.path.join("generated_pdfs", filename)

    if not os.path.exists(file_path):
        return {"error": "File not found."}

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )


# --------------------------------------------------
# 🛡 GLOBAL ERROR HANDLER (Prevents 500 Crash)
# --------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("Global Error:", str(exc))
    return JSONResponse(
        status_code=200,
        content={"type": "text", "message": "AI temporarily unavailable."}
    )

#ingest all pdfs
@app.post("/admin/ingest-all")
def ingest_all():
    return ingest_all_pdfs()

#getting grades
from qdrant_client import QdrantClient

 

@app.get("/grades")
def get_grades():

    collections = client.get_collections().collections
    grades = set()

    for col in collections:
        scroll = client.scroll(collection_name=col.name, limit=10)

        for point in scroll[0]:
            if "grade" in point.payload:
                grades.add(str(point.payload["grade"]))

    return sorted(list(grades))


#get subjects for a grade
@app.get("/subjects")
def get_subjects(grade: int):

    collections = client.get_collections().collections
    subjects = []

    for col in collections:
        parts = col.name.split("_")
        if len(parts) == 3 and int(parts[1]) == grade:
            subjects.append(parts[2])

    return subjects

#get chapters for a grade and subject
from qdrant_client.models import Filter, FieldCondition, MatchValue


@app.get("/chapters")
def get_chapters(grade: int, subject: str):

    collection_name = f"olympiad_{grade}_{subject}"

    results = client.scroll(
        collection_name=collection_name,
        limit=100
    )

    chapters = set()

    for point in results[0]:
        chapters.add(point.payload["chapter_name"])

    return list(chapters)

#get full content for a chapter
@app.get("/chapter-content")
def get_chapter_content(grade: int, subject: str, chapter_name: str):

    collection_name = f"olympiad_{grade}_{subject}"

    results = client.scroll(
        collection_name=collection_name,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="chapter_name",
                    match=MatchValue(value=chapter_name)
                ),
                FieldCondition(
                    key="type",
                    match=MatchValue(value="full_chapter")
                )
            ]
        ),
        limit=1
    )

    if not results[0]:
        return {"content": "Not found"}

    return {"content": results[0][0].payload["content"]}


#router register
from app.routers import chat_router

app.include_router(chat_router.router)









@app.get("/debug-collections")
def debug_collections():
    collections = client.get_collections().collections
    return [c.name for c in collections]
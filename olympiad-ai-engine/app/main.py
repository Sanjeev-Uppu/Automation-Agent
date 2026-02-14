from dotenv import load_dotenv
load_dotenv()

import json
import re
from typing import List, Optional
from app.services.planner_engine import generate_llm_plan
from app.services.deterministic_planner import generate_fallback_plan

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models.request_models import AskRequest
from app.models.mock_models import MockRequest, SubmissionRequest

from app.embeddings.embedder import generate_embedding
from app.vectorstore.qdrant_client import search_similar

from app.services.qa_engine import generate_answer
from app.services.ingest import ingest_pdf

# 🔥 LLM mock engine
from app.services.mock_engine import generate_mock_exam as generate_llm_mock

# 🔥 Deterministic fallback engine
from app.services.deterministic_mock_engine import generate_mock_exam as generate_fallback_mock

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
# 📦 RESPONSE MODEL
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
# 🧠 HELPER: Extract List From Context
# --------------------------------------------------

def extract_list_from_context(text: str):
    pattern = r'Example:\s*(.*)'
    matches = re.findall(pattern, text)

    items = []
    for match in matches:
        parts = match.split(",")
        for item in parts:
            cleaned = item.strip().capitalize()
            if cleaned and cleaned not in items:
                items.append(cleaned)

    return items


# --------------------------------------------------
# 💬 ASK ENDPOINT
# --------------------------------------------------

@app.post("/ask/", response_model=AskResponse)
def ask_question(request: AskRequest):

    collection_name = f"olympiad_{request.grade}_{request.subject}"

    # Convert question to embedding
    query_vector = generate_embedding(request.question)

    is_list_query = "list" in request.question.lower()

    limit = 1 if is_list_query else 3

    results = search_similar(
        collection_name,
        query_vector,
        request.chapter_name,
        limit=limit
    )

    if not results:
        raise HTTPException(status_code=404, detail="Not available in the lesson.")

    context_text = "\n\n".join([r["content"] for r in results])

    # 🔹 LIST MODE
    if is_list_query:
        structured_list = extract_list_from_context(context_text)

        return AskResponse(
            question=request.question,
            answer_type="list",
            count=len(structured_list),
            data=structured_list
        )

    # 🔹 EXPLANATION MODE (LLM)
    answer = generate_answer(context_text, request.question)

    return AskResponse(
        question=request.question,
        answer_type="explanation",
        explanation=answer
    )


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

    # --------------------------------------------------
    # 🔥 TRY LLM FIRST
    # --------------------------------------------------

    try:
        mock_json_string = generate_llm_mock(context_text, request.chapter_name)

        mock_data = json.loads(mock_json_string)

        print("✅ LLM Mock Used")
        return mock_data

    except ClientError:
        print("⚠️ Gemini quota exceeded. Switching to fallback.")

    except Exception as e:
        print("⚠️ LLM failed. Using fallback engine.")
        print("Error:", str(e))

    # --------------------------------------------------
    # 🔥 FALLBACK ENGINE
    # --------------------------------------------------

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
        # 🔥 Try LLM first
        plan_json = generate_llm_plan(duration_days, chapter_name)
        return json.loads(plan_json)

    except Exception:
        # 🔥 Fallback
        return generate_fallback_plan(duration_days, chapter_name)


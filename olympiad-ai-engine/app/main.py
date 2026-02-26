from dotenv import load_dotenv
load_dotenv()
import os
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from app.services.question_paper_modify_engine import regenerate_question_paper_with_modifications
from app.vectorstore.qdrant_client import client, search_similar
#from app.vectorstore.qdrant_client import get_client, search_similar
from app.models.request_models import AskRequest
from app.models.mock_models import (
    MockRequest,
    SubmissionRequest,
    QuestionPaperRequest
)
from app.embeddings.embedder import generate_embedding
from app.services.planner_engine import generate_llm_plan
from app.services.qa_engine import generate_answer
from app.services.mock_engine import generate_mock_exam_llm
from app.services.deterministic_mock_engine import generate_mock_exam as generate_fallback_mock
from app.services.question_paper_engine import generate_question_paper_llm
from app.services.pdf_exam_generator import generate_question_paper_pdf
from qdrant_client.models import Filter, FieldCondition, MatchValue


app = FastAPI(title="Olympiad Mastery AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {"message": "Olympiad AI Engine Running Successfully"}


# --------------------------------------------------
# ASK ENDPOINT
# --------------------------------------------------

@app.post("/ask/")
def ask_question(request: AskRequest):

    user_query = request.question.lower()

    # Detect Question Paper Intent
    if "question paper" in user_query:
        return {
            "type": "question_paper_setup",
            "message": "Please configure your question paper."
        }

    # Normal QA
    query_vector = generate_embedding(request.question)

    results = search_similar(
        grade=request.grade,
        subject=request.subject,
        chapter_name=request.chapter_name,
        query_vector=query_vector,
        limit=5
    )

    context_text = "\n\n".join(
        [r["content"] for r in results]
    )[:4000]

    answer = generate_answer(context_text, request.question)

    return {"type": "text", "message": answer}


# --------------------------------------------------
# GENERATE MOCK TEST
# --------------------------------------------------

@app.post("/generate-mock/")
def generate_mock(request: MockRequest):

    results = search_similar(
        grade=request.grade,
        subject=request.subject,
        chapter_name=request.chapter_name,
        query_vector=generate_embedding(request.chapter_name),
        limit=10
    )

    context_text = "\n\n".join(
        [r["content"] for r in results]
    )[:4000]

    try:
        return generate_mock_exam_llm(
            context=context_text,
            chapter_name=request.chapter_name,
            num_questions=request.number_of_questions,
            duration_minutes=request.duration_minutes,
            grade=request.grade,
            subject=request.subject
        )
    except Exception:
        return generate_fallback_mock(
            chapter_name=request.chapter_name,
            num_questions=request.number_of_questions,
            duration_minutes=request.duration_minutes,
            grade=request.grade,
            subject=request.subject
        )


# --------------------------------------------------
# SUBMIT MOCK
# --------------------------------------------------

@app.post("/submit-mock/")
def submit_mock(submission: SubmissionRequest):

    score = sum(
        1 for q in submission.questions
        if q.selected_answer == q.correct_answer
    )

    total = len(submission.questions)

    return {
        "total_questions": total,
        "correct": score,
        "percentage": round((score / total) * 100, 2) if total > 0 else 0
    }


# --------------------------------------------------
# GENERATE QUESTION PAPER (SEPARATE ENGINE)
# --------------------------------------------------
@app.post("/generate-question-paper/")
def generate_question_paper(request: QuestionPaperRequest):

    results = search_similar(
        grade=request.grade,
        subject=request.subject,
        chapter_name=request.chapter_name,
        query_vector=generate_embedding(request.chapter_name),
        limit=10
    )

    context_text = "\n\n".join(
        [r["content"] for r in results]
    )[:4000]

    paper_data = generate_question_paper_llm(
        context=context_text,
        chapter_name=request.chapter_name,
        num_questions=request.number_of_questions,
        duration_minutes=request.duration_minutes,
        grade=request.grade,
        subject=request.subject,
        marks_per_question=request.marks_per_question,
        difficulty_level=request.difficulty_level
    )

    return {
        "type": "question_paper_preview",
        "paper_data": paper_data
    }


#--------------------------------------------------
#modify question paper endpoint to generate and return PDF
#--------------------------------------------------
@app.post("/modify-question-paper/")
def modify_question_paper(request: dict):

    original_paper = request["original_paper"]
    modification_request = request["modification_request"]

    updated_paper = regenerate_question_paper_with_modifications(
        original_paper,
        modification_request
    )

    return {
        "paper_data": updated_paper
    }
#----------------------------------------------


@app.post("/generate-question-paper-pdf/")
def generate_question_paper_pdf_endpoint(request: dict):

    paper_data = request["paper_data"]

    filename = f"question_paper_{uuid.uuid4().hex}.pdf"
    os.makedirs("generated_pdfs", exist_ok=True)

    file_path = os.path.join("generated_pdfs", filename)

    generate_question_paper_pdf(
        paper_data,
        file_path=file_path
    )

    return {
    "download_url": f"/download/{filename}"
}

"""
@app.get("/download/{filename}")
def download_file(filename: str):

    file_path = os.path.join("generated_pdfs", filename)

    if not os.path.exists(file_path):
        return {"error": "File not found."}

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f"inline; filename={filename}"
        }
    )

"""

# --------------------------------------------------
# GET GRADES
# --------------------------------------------------

@app.get("/grades")
def get_grades():
    collections = client.get_collections().collections
    grades = [
        col.name.replace("olympiad_grade_", "")
        for col in collections
        if col.name.startswith("olympiad_grade_")
    ]
    return sorted(grades)


# --------------------------------------------------
# GET SUBJECTS
# --------------------------------------------------

@app.get("/subjects")
def get_subjects(grade: int):

    collection_name = f"olympiad_grade_{grade}"

    results = client.scroll(
        collection_name=collection_name,
        limit=500
    )

    subjects = {
        point.payload["subject"]
        for point in results[0]
    }

    return sorted(list(subjects))


# --------------------------------------------------
# GET CHAPTERS
# --------------------------------------------------

@app.get("/chapters")
def get_chapters(grade: int, subject: str):

    collection_name = f"olympiad_grade_{grade}"

    results = client.scroll(
        collection_name=collection_name,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="subject",
                    match=MatchValue(value=subject.lower())
                )
            ]
        ),
        limit=1000
    )

    chapters = {
        point.payload["chapter_name"]
        for point in results[0]
    }

    return sorted(list(chapters))


# --------------------------------------------------
# GLOBAL ERROR HANDLER
# --------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("Global Error:", str(exc))
    return JSONResponse(
        status_code=500,
        content={"message": "AI temporarily unavailable."}
    )
# --------------------------------------------------
# DOWNLOAD GENERATED PDF
# --------------------------------------------------

from fastapi.responses import FileResponse

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

from app.models.planner_models import PlannerRequest

@app.post("/generate-plan/")
def generate_plan(request: PlannerRequest):

   return generate_llm_plan(
    duration_days=request.duration_days,
    chapter_name=request.chapter_name,
    grade=request.grade,
    subject=request.subject
)
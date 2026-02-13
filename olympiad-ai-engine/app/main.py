from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from app.models.request_models import AskRequest
from app.embeddings.embedder import generate_embedding
from app.vectorstore.qdrant_client import search_similar
from app.services.qa_engine import generate_answer
from app.services.ingest import ingest_pdf
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import re


#app = FastAPI(title="Olympiad Mastery AI Engine")

app = FastAPI(title="Olympiad Mastery AI Engine")

 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=False,  # MUST be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)



# -------------------------------
# 🔹 RESPONSE MODEL (PRO LEVEL)
# -------------------------------

class AskResponse(BaseModel):
    question: str
    answer_type: str
    count: Optional[int] = None
    data: Optional[List[str]] = None
    explanation: Optional[str] = None


# -------------------------------
# 🔹 ROOT
# -------------------------------

@app.get("/")
def root():
    return {"message": "Olympiad AI Engine Running Successfully"}


# -------------------------------
# 🔹 INGEST
# -------------------------------

@app.post("/ingest/")
def ingest():
    return ingest_pdf(
        file_path="data/pdfs/Animals.pdf",
        grade=5,
        subject="science",
        chapter_name="Animals"
    )


# -------------------------------
# 🔹 HELPER: Extract List Cleanly
# -------------------------------

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


# -------------------------------
# 🔹 ASK ENDPOINT
# -------------------------------

@app.post("/ask/", response_model=AskResponse)
def ask_question(request: AskRequest):

    collection_name = f"olympiad_{request.grade}_{request.subject}"

    # Step 1: Convert question → embedding
    query_vector = generate_embedding(request.question)

    # Step 2: Adjust retrieval depth
    is_list_query = "list" in request.question.lower()

    limit = 1 if is_list_query else 3

    # Step 3: Search vector DB
    results = search_similar(
        collection_name,
        query_vector,
        request.chapter_name,
        limit=limit
    )

    if not results:
        raise HTTPException(status_code=404, detail="Not available in the lesson.")

    # Step 4: Combine context
    context_text = "\n\n".join([r["content"] for r in results])

    # Step 5: If listing question → structured output
    if is_list_query:
        structured_list = extract_list_from_context(context_text)

        return AskResponse(
            question=request.question,
            answer_type="list",
            count=len(structured_list),
            data=structured_list
        )

    # Step 6: Explanation mode (LLM)
    answer = generate_answer(context_text, request.question)

    return AskResponse(
        question=request.question,
        answer_type="explanation",
        explanation=answer
    )

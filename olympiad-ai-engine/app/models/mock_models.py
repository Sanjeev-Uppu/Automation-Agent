from pydantic import BaseModel
from typing import List

class MockRequest(BaseModel):
    grade: int
    subject: str
    chapter_name: str

class AnswerItem(BaseModel):
    question_id: int
    selected_answer: str
    correct_answer: str

class SubmissionRequest(BaseModel):
    questions: List[AnswerItem]

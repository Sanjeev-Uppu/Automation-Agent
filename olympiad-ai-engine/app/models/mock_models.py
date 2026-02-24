from pydantic import BaseModel
from typing import List
from typing import Optional

from pydantic import BaseModel


class QuestionPaperRequest(BaseModel):
    grade: int
    subject: str
    chapter_name: str
    number_of_questions: int
    duration_minutes: int
    marks_per_question: int
    difficulty_level: str
# -----------------------------
# REQUEST FOR MOCK GENERATION
# -----------------------------
class MockRequest(BaseModel):
    grade: int
    subject: str
    chapter_name: str
    number_of_questions: int
    duration_minutes: int


# -----------------------------
# ANSWER SUBMISSION
# -----------------------------
class AnswerItem(BaseModel):
    question_id: int
    selected_answer: str
    correct_answer: str


 
class SubmissionRequest(BaseModel):
    questions: List[AnswerItem]

 
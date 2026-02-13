from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    question: str
    grade: int
    subject: str
    chapter_name: Optional[str] = None

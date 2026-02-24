from pydantic import BaseModel

class PlannerRequest(BaseModel):
    grade: int
    subject: str
    chapter_name: str
    duration_days: int
# app/models/quiz.py
from pydantic import BaseModel
from typing import Optional
import datetime

class QuizResponse(BaseModel):
    user_id: str
    quiz_id: str
    responses: dict
    notes: dict
    status: str
    last_question_index: int
    total_scores: dict
    started_at: datetime.datetime
    finished_at: Optional[datetime.datetime] = None

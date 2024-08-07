# app/router/router_quiz.py
from fastapi import APIRouter, HTTPException
import os
import json

router = APIRouter()

@router.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        quiz_file_path = os.path.join(current_dir, "..", "quiztext", f"{quiz_id}.json")
        
        if not os.path.exists(quiz_file_path):
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        with open(quiz_file_path, "r") as file:
            quiz_data = json.load(file)
        
        return quiz_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Quiz not found")

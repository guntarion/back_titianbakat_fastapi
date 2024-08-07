# app/router/router_quizresponse.py
from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from app.models.quiz import QuizResponse  # Update import
from db.database import quiz_responses_collection
import datetime

router = APIRouter()

@router.post("/quizresponse/new")
async def create_new_quiz_response(response: QuizResponse):
    try:
        response_data = response.dict()
        response_data["_id"] = ObjectId()
        quiz_responses_collection.insert_one(response_data)
        return {"message": "New quiz response created successfully", "id": str(response_data["_id"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/quizresponse")
async def update_quiz_response(response: QuizResponse):
    try:
        existing_response = quiz_responses_collection.find_one({"user_id": response.user_id, "quiz_id": response.quiz_id, "status": "in progress"})
        if existing_response:
            quiz_responses_collection.update_one(
                {"_id": existing_response["_id"]},
                {"$set": {
                    "responses": response.responses,
                    "notes": response.notes,
                    "status": response.status,
                    "last_question_index": response.last_question_index,
                    "total_scores": response.total_scores,
                    "finished_at": response.finished_at
                }}
            )
            return {"message": "Quiz response updated successfully", "id": str(existing_response["_id"])}
        else:
            raise HTTPException(status_code=404, detail="Quiz response not found for update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quizresponse/{user_id}/{quiz_id}")
async def get_quiz_response(user_id: str, quiz_id: str):
    try:
        response = quiz_responses_collection.find({"user_id": user_id, "quiz_id": quiz_id}).sort("started_at", -1).limit(1)
        response_list = list(response)
        if response_list and response_list[0]:
            response_data = response_list[0]
            response_data["_id"] = str(response_data["_id"])
            return response_data
        else:
            raise HTTPException(status_code=404, detail="Quiz response not found")
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

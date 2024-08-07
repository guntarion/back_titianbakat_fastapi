# app/router/router_followup.py

from fastapi import APIRouter, HTTPException
import os
import json

router = APIRouter()

@router.get("/followup/{type}/{category}")
async def get_followup(type: str, category: str):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, "..", "quiztext", "followup_multipleintelligences.json")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        followups = data.get("followup_multipleintelligences", [])
        for followup in followups:
            if followup["type"] == type:
                return followup.get(category, "")

        raise HTTPException(status_code=404, detail="Follow-up not found")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Follow-up data file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

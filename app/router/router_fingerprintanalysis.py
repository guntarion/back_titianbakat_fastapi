# app/router/router_quizresponse.py
from fastapi import APIRouter, Request, UploadFile, File
from app.processor.processor_fgpr import process_fingerprint_data
from app.processor.processor_openai import analyze_fingerprint

router = APIRouter()

@router.post("/api/finger-type-ridge")
async def finger_type_ridge(request: Request):
    data = await request.json()
    processed_data = process_fingerprint_data(data)
    return {"processed_data": processed_data}

@router.post("/api/analyze-fingerprint")
async def analyze_fingerprint_endpoint(file: UploadFile = File(...)):
    return await analyze_fingerprint(file)

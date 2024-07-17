from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.processor.processor_fgpr import process_fingerprint_data
from app.processor.processor_openai import analyze_fingerprint
from app.router.router_user import router as user_router  # Import the user router

import json
import os

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the user router
app.include_router(user_router, prefix="/api", tags=["users"])

@app.get("/")
async def root():
    return {"message": "FastAPI JAPO Server is running smoothly."}

@app.post("/api/finger-type-ridge")
async def finger_type_ridge(request: Request):
    data = await request.json()
    processed_data = process_fingerprint_data(data)
    return {"processed_data": processed_data}

@app.post("/api/analyze-fingerprint")
async def analyze_fingerprint_endpoint(file: UploadFile = File(...)):
    return await analyze_fingerprint(file)

@app.get("/api/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str):
    try:
        file_path = f"./app/quiztext/{quiz_id}.json"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050)

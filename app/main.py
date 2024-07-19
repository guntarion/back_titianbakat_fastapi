from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.router.router_fingerprintanalysis import router as fingerprintanalysis_router
from app.router.router_user import router as user_router 
from app.router.router_quiz import router as quiz_router
from app.router.router_quizresponse import router as quizresponse_router

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
app.include_router(fingerprintanalysis_router, prefix="/api", tags=["fingerprintanalysis"])
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(quiz_router, prefix="/api", tags=["quiz"])
app.include_router(quizresponse_router, prefix="/api", tags=["quizresponse"])

@app.get("/")
async def root():
    return {"message": "FastAPI JAPO Server is running smoothly."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050)

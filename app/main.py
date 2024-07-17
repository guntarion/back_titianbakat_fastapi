from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.processor.processor_fgpr import process_fingerprint_data
from app.processor.processor_openai import analyze_fingerprint
from app.router.router_user import router as user_router  # Import the user router

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050)

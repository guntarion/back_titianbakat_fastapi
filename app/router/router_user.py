# app/router/router_user.py
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.user import User
from db.database import users_collection, client

router = APIRouter()

@router.post("/users/")
async def create_user(user: User):
    existing_user = users_collection.find_one({"alamatEmail": user.alamatEmail})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_data = user.dict()
    result = users_collection.insert_one(user_data)
    return {"id": str(result.inserted_id)}

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    existing_user = users_collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/test-connection/")
async def test_connection():
    try:
        client.admin.command('ping')
        return {"message": "Connection to MongoDB is successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

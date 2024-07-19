# app/db/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("db-titian-bakat")

users_collection = db.get_collection("user")
quiz_responses_collection = db.get_collection("quiz_responses")

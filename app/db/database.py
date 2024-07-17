# app/db/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
# print("Mongo URI:", MONGO_URI)  # Debugging print statement
client = MongoClient(MONGO_URI)
db = client.get_database("db-titian-bakat")  # Replace with your actual database name
users_collection = db.get_collection("user")

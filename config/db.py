from pymongo import MongoClient
import os
url = os.getenv("DB_URL")

client = MongoClient(url)
db = client["fastAPI"]  # Create a database called fastAPI
users = db["users"]  # Create a collection called users

from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.mongodb_url)
db = client[settings.database_name]
users_collection = db["users"]

# Employee ID should be unique.
users_collection.create_index("employee_id", unique=True)

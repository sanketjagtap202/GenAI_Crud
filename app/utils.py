from datetime import date
from bson import ObjectId
from fastapi import HTTPException

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "user_name": user["user_name"],
        "address": user["address"],
        "employee_id": user["employee_id"],
        "salary": user["salary"],
        "gender": user["gender"],
        "joining_date": user["joining_date"],
        "active_status": user["active_status"],
        "profile_photo": user.get("profile_photo"),
    }


def parse_object_id(user_id: str) -> ObjectId:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    return ObjectId(user_id)


def validate_image(content_type: str | None):
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WEBP and GIF images are allowed")

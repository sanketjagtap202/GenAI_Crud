from datetime import datetime, date, time
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pymongo.errors import DuplicateKeyError

from .config import settings
from .database import users_collection
from .schemas import UserCreate, UserUpdate, UserResponse
from .utils import parse_object_id, serialize_user, validate_image

router = APIRouter(prefix="/api/users", tags=["Users"])
UPLOAD_DIR = Path(settings.upload_dir)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_BYTES = settings.max_file_size_mb * 1024 * 1024

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    doc = user.model_dump()
    doc["joining_date"] = datetime.combine(doc["joining_date"], time.min)
    doc["profile_photo"] = None

    try:
        result = users_collection.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Employee ID already exists")

    created = users_collection.find_one({"_id": result.inserted_id})
    return serialize_user(created)

@router.get("", response_model=list[UserResponse])
def get_users():
    return [serialize_user(u) for u in users_collection.find().sort("_id", -1)]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    user = users_collection.find_one({"_id": parse_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate):
    oid = parse_object_id(user_id)

    updates = {
        k: v
        for k, v in user.model_dump(exclude_unset=True).items()
        if v is not None
    }

    if "joining_date" in updates:
        updates["joining_date"] = datetime.combine(updates["joining_date"], time.min)

    if not updates:
        raise HTTPException(status_code=400, detail="At least one field is required")

    try:
        result = users_collection.update_one(
            {"_id": oid},
            {"$set": updates}
        )
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Employee ID already exists")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return serialize_user(users_collection.find_one({"_id": oid}))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    oid = parse_object_id(user_id)
    user = users_collection.find_one({"_id": oid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.get("profile_photo"):
        path = Path(user["profile_photo"])
        if path.exists():
            path.unlink()
    users_collection.delete_one({"_id": oid})

@router.post("/{user_id}/profile-photo", response_model=UserResponse)
def upload_profile_photo(user_id: str, file: UploadFile = File(...)):
    oid = parse_object_id(user_id)
    user = users_collection.find_one({"_id": oid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    validate_image(file.content_type)

    content = file.file.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"Image must be <= {settings.max_file_size_mb} MB")

    extension = Path(file.filename or "image").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        extension = ".jpg" if file.content_type == "image/jpeg" else ".png"
    target = UPLOAD_DIR / f"{oid}_{uuid4().hex}{extension}"
    target.write_bytes(content)

    old = user.get("profile_photo")
    if old and Path(old).exists():
        Path(old).unlink()
    users_collection.update_one({"_id": oid}, {"$set": {"profile_photo": str(target)}})
    return serialize_user(users_collection.find_one({"_id": oid}))

@router.put("/{user_id}/profile-photo", response_model=UserResponse)
def update_profile_photo(user_id: str, file: UploadFile = File(...)):
    return upload_profile_photo(user_id, file)

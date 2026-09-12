from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=2, max_length=300)
    employee_id: str = Field(..., min_length=1, max_length=50)
    salary: float = Field(..., ge=0)
    gender: str = Field(..., min_length=1, max_length=20)
    joining_date: date
    active_status: bool = True

class UserUpdate(BaseModel):
    user_name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, min_length=2, max_length=300)
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)
    salary: Optional[float] = Field(None, ge=0)
    gender: Optional[str] = Field(None, min_length=1, max_length=20)
    joining_date: Optional[date] = None
    active_status: Optional[bool] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    user_name: str
    address: str
    employee_id: str
    salary: float
    gender: str
    joining_date: date
    active_status: bool
    profile_photo: Optional[str] = None

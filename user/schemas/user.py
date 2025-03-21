from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    role: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    role: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ListUserResponse(BaseModel):
    users: list[UserResponse]
    tolal_data: int

    class Config:
        from_attributes = True


class UserPageableResponse(BaseModel):
    users: list[UserResponse]

    total_pages: int
    total_data: int

    class Config:
        from_attributes = True


class UserSearch(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

    
class UserDelete(BaseModel):
    list_id: list[int]

    class Config:
        from_attributes = True

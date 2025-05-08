# this file contains the schemas for the todo application
# and is used to define the data models for the application.
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Todo(BaseModel):
    description: str
    deadline: datetime
    done: bool

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes

class Token(BaseModel):
    access_token: str
    refresh_token: str  
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    token_type: Optional[str] = None  # Added to distinguish between access and refresh tokens
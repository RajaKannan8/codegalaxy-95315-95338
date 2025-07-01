from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import List


# PUBLIC_INTERFACE
class Role(str, Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"
    DEVELOPER = "developer"


# PUBLIC_INTERFACE
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: List[Role]


# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# PUBLIC_INTERFACE
class LoginRequest(BaseModel):
    username: str = Field(..., example="someone")
    password: str = Field(..., example="password")


# PUBLIC_INTERFACE
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User


# PUBLIC_INTERFACE
class Token(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str         # Will be "bearer" usually

class RefreshTokenRequest(BaseModel):
    refresh_token: str


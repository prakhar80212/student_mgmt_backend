from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from models import UserRole


# ── Auth ────────────────────────────────────────────────────────────────────

class SignupRequest(BaseModel):
    name:     str       = Field(..., min_length=2, max_length=120)
    email:    EmailStr
    password: str       = Field(..., min_length=6)
    role:     UserRole  = UserRole.user   # callers can pass "admin" for demo


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"
    user:          "UserOut"


# ── Users ────────────────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id:         int
    name:       str
    email:      str
    role:       UserRole
    created_at: datetime

    class Config:
        from_attributes = True


# ── Students ─────────────────────────────────────────────────────────────────

class StudentBase(BaseModel):
    name:        str   = Field(..., min_length=2, max_length=120)
    email:       EmailStr
    roll_number: str   = Field(..., min_length=2, max_length=50)
    department:  str   = Field(..., min_length=2, max_length=120)
    semester:    int   = Field(..., ge=1, le=12)
    gpa:         float = Field(..., ge=0.0, le=10.0)
    phone:       Optional[str] = None
    address:     Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    """All fields optional for PATCH-style update."""
    name:       Optional[str]   = Field(None, min_length=2, max_length=120)
    email:      Optional[EmailStr] = None
    department: Optional[str]   = Field(None, min_length=2, max_length=120)
    semester:   Optional[int]   = Field(None, ge=1, le=12)
    gpa:        Optional[float] = Field(None, ge=0.0, le=10.0)
    phone:      Optional[str]   = None
    address:    Optional[str]   = None


class StudentOut(StudentBase):
    id:         int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# resolve forward ref
TokenResponse.model_rebuild()

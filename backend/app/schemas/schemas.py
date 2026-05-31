from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ── AUTH ──────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


# ── PROJECTS ──────────────────────────────────────────────────
class ProjectBase(BaseModel):
    number: Optional[str] = None
    name: str
    description: str
    stack: List[str] = []
    link: str = "#"
    link_label: str = "View Project"
    featured: bool = False
    is_active: bool = True
    order: int = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


# ── BLOG ──────────────────────────────────────────────────────
class BlogBase(BaseModel):
    title: str
    excerpt: str
    content: str = ""
    category: str = "Engineering"
    read_time: str = "5 min read"
    slug: str
    published: bool = False

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    slug: Optional[str] = None

class BlogOut(BlogBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


# ── CONTACT ───────────────────────────────────────────────────
class ContactRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=300)
    message: str = Field(min_length=10)

class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True

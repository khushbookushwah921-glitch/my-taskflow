from pydantic import BaseModel, Field, field_validator
from typing import Optional


# =========================
# USER
# =========================

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


# =========================
# PROJECT
# =========================

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Project name cannot be empty")
        return value.strip()


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# TASK CREATE
# =========================

class TaskCreate(BaseModel):
    title: str
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


# =========================
# TASK RESPONSE
# =========================

class TaskResponse(TaskCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


# =========================
# TASK STATUS UPDATE
# =========================

class TaskStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(pending|in_progress|completed)$"
    )


# =========================
# TASK UPDATE / EDIT
# =========================

class TaskUpdate(BaseModel):
    title: Optional[str] = None

    priority: Optional[str] = Field(
        default=None,
        pattern="^(low|medium|high)$"
    )

    due_date: Optional[str] = None

    project_id: Optional[int] = None

    status: Optional[str] = Field(
        default=None,
        pattern="^(pending|in_progress|completed)$"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip() if value is not None else None


# =========================
# AI QUICK ADD
# =========================

class QuickAddRequest(BaseModel):
    description: str
    project_id: int

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if not value.strip():
            raise ValueError("Description cannot be empty")
        return value.strip()
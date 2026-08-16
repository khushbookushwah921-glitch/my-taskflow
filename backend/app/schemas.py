from pydantic import BaseModel, Field, field_validator
from typing import Optional


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


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    priority: str = Field(pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value


class TaskResponse(TaskCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

class TaskStatusUpdate(BaseModel):
    status: str = Field(pattern="^(pending|in_progress|completed)$")

class QuickAddRequest(BaseModel):
    description: str
    project_id: int

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if not value.strip():
            raise ValueError("Description cannot be empty")
        return value
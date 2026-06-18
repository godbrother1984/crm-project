"""Pydantic schemas for User."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a user."""

    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(default="sales", pattern=r"^(admin|sales|manager)$")
    avatar_url: str | None = Field(None, max_length=500)


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    display_name: str | None = Field(None, min_length=1, max_length=255)
    role: str | None = Field(None, pattern=r"^(admin|sales|manager)$")
    is_active: bool | None = None
    avatar_url: str | None = Field(None, max_length=500)


class UserRead(BaseModel):
    """Schema for reading a user."""

    id: uuid.UUID
    email: str
    display_name: str
    role: str
    is_active: bool
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

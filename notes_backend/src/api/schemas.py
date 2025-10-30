from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base fields for Note payloads."""
    title: str = Field(..., description="Title of the note", min_length=1, max_length=255)
    content: str = Field("", description="Content/body of the note")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating an existing note."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="Updated content/body of the note")


class NoteRead(NoteBase):
    """Schema for reading a note."""
    id: int = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models

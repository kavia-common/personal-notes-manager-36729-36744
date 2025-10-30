from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas


# PUBLIC_INTERFACE
def create_note(db: Session, note_in: schemas.NoteCreate) -> models.Note:
    """Create a new note in the database."""
    note = models.Note(title=note_in.title, content=note_in.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    """Retrieve a single note by its ID."""
    return db.get(models.Note, note_id)


# PUBLIC_INTERFACE
def list_notes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Note]:
    """List notes with pagination."""
    stmt = select(models.Note).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


# PUBLIC_INTERFACE
def update_note(db: Session, note: models.Note, note_in: schemas.NoteUpdate) -> models.Note:
    """Update an existing note instance with provided fields."""
    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
def delete_note(db: Session, note: models.Note) -> None:
    """Delete the provided note from the database."""
    db.delete(note)
    db.commit()

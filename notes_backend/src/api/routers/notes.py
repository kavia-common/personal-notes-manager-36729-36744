from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, Response
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=schemas.NoteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with a title and content.",
    responses={
        201: {"description": "Note created successfully"},
        422: {"description": "Validation Error"},
    },
)
def create_note_endpoint(note_in: schemas.NoteCreate, db: Session = Depends(get_db)) -> schemas.NoteRead:
    """Create a new note and return the created resource."""
    note = crud.create_note(db, note_in)
    return note


@router.get(
    "",
    response_model=List[schemas.NoteRead],
    summary="List notes",
    description="List notes with pagination using skip and limit parameters.",
)
def list_notes_endpoint(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
) -> List[schemas.NoteRead]:
    """Return a list of notes with pagination."""
    notes = crud.list_notes(db, skip=skip, limit=limit)
    return notes


@router.get(
    "/{note_id}",
    response_model=schemas.NoteRead,
    summary="Get a note",
    description="Retrieve a single note by its ID.",
    responses={
        404: {"description": "Note not found"},
    },
)
def get_note_endpoint(
    note_id: int = Path(..., ge=1, description="ID of the note to retrieve"),
    db: Session = Depends(get_db),
) -> schemas.NoteRead:
    """Return a single note by ID or 404 if not found."""
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.put(
    "/{note_id}",
    response_model=schemas.NoteRead,
    summary="Update a note",
    description="Update an existing note's title and/or content by ID.",
    responses={
        404: {"description": "Note not found"},
    },
)
def update_note_endpoint(
    note_id: int = Path(..., ge=1, description="ID of the note to update"),
    note_in: schemas.NoteUpdate = ...,
    db: Session = Depends(get_db),
) -> schemas.NoteRead:
    """Update a note by ID or return 404 if it does not exist."""
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    note = crud.update_note(db, note, note_in)
    return note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its ID.",
    responses={
        204: {"description": "Note deleted successfully"},
        404: {"description": "Note not found"},
    },
)
def delete_note_endpoint(
    note_id: int = Path(..., ge=1, description="ID of the note to delete"),
    db: Session = Depends(get_db),
) -> None:
    """Delete a note by ID or return 404 if it does not exist."""
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud.delete_note(db, note)
    # For 204 No Content, FastAPI must not send a body
    return Response(status_code=status.HTTP_204_NO_CONTENT)

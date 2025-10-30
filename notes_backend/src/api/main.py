from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import notes as notes_router

APP_TITLE = "Notes Backend API"
APP_DESCRIPTION = (
    "A FastAPI backend that provides CRUD operations for personal notes. "
    "Includes endpoints to create, list, retrieve, update, and delete notes with SQLite persistence."
)
APP_VERSION = "1.0.0"

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    openapi_tags=[
        {"name": "Health", "description": "Service health checks"},
        {"name": "Notes", "description": "Operations on notes"},
    ],
)

# CORS configuration (allow all by default; refine as needed via env vars)
allow_origins = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on application startup."""
    init_db()


@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Basic endpoint to verify that the service is running.",
)
def health_check():
    """Return a simple health check response."""
    return {"message": "Healthy"}


# Register notes router
app.include_router(notes_router.router)

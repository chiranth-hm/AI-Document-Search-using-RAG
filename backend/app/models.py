"""Request/response models for the API."""
from pydantic import BaseModel
from typing import Optional


class IngestResponse(BaseModel):
    """Response after ingesting PDF(s)."""
    success: bool
    message: str
    num_documents: int = 0
    num_chunks: int = 0


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str  # "user" | "assistant"
    content: str
    sources: Optional[list[str]] = None


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str
    session_id: Optional[str] = None


class SourceChunk(BaseModel):
    """A retrieved source chunk."""
    content: str
    metadata: Optional[dict] = None


class ChatResponse(BaseModel):
    """Streaming or final chat response."""
    message: str
    sources: Optional[list[SourceChunk]] = None
    done: bool = False

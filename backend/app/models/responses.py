# backend/app/models/responses.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GenerateContentResponse(BaseModel):
    id: str
    content: str
    content_type: str
    model: str
    usage: dict
    created_at: datetime

class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[dict] = None

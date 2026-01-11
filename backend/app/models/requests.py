# backend/app/models/requests.py
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ContentType(str, Enum):
    BLOG = "blog"
    SOCIAL = "social"
    EMAIL = "email"
    MARKETING = "marketing"

class Tone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FORMAL = "formal"
    FRIENDLY = "friendly"

class GenerateContentRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=5000)
    content_type: ContentType
    tone: Tone = Tone.PROFESSIONAL
    max_tokens: int = Field(default=1000, ge=50, le=4000)
    template_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write about the benefits of AI in marketing",
                "content_type": "blog",
                "tone": "professional",
                "max_tokens": 1000
            }
        }

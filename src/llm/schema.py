from pydantic import BaseModel, Field, validator
from typing import Literal

class ClassifyInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()

class ClassifyOutput(BaseModel):
    category: Literal["billing", "bug", "feature", "other"]
    urgency: Literal["low", "normal", "high"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(..., max_length=200)
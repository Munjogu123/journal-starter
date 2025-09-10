from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import uuid4

class EntryCreate(BaseModel):
    """Model for creating a new journal entry (user input)."""
    work: str = Field(
        max_length=256,
        description="What did you work on today?",
        json_schema_extra={"example": "Studied FastAPI and built my first API endpoints"}
    )
    struggle: str = Field(
        max_length=256,
        description="What's one thing you struggled with today?",
        json_schema_extra={"example": "Understanding async/await syntax and when to use it"}
    )
    intention: str = Field(
        max_length=256,
        description="What will you study/work on tomorrow?",
        json_schema_extra={"example": "Practice PostgreSQL queries and database design"}
    )

class Entry(BaseModel):
    # TODO: Add field validation rules
    # TODO: Add custom validators
    # TODO: Add schema versioning
    # TODO: Add data sanitization methods

    # Schema Versioning
    version: str = Field(
        default="1.0",
        description="Schema version of entry model"
    )
    
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the entry (UUID)."
    )
    work: str = Field(
        min_length=5,
        max_length=256,
        description="What did you work on today?"
    )
    struggle: str = Field(
        min_length=5,
        max_length=256,
        description="What’s one thing you struggled with today?"
    )
    intention: str = Field(
        min_length=5,
        max_length=256,
        description="What will you study/work on tomorrow?"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the entry was created."
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the entry was last updated."
    )

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }

    # Data Sanitization Methods
    @field_validator("work", "struggle", "intention", mode="before")
    def strip_and_normalize(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        return v.strip()
    
    # Custom Validator
    @field_validator("updated_at")
    def updated_at_after_created_at(cls, v, values):
        created_at = values.get("created_at")
        if created_at and v < created_at:
            raise ValueError("updated_at cannot be before created_at")
        return v

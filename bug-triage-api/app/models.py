from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
import uuid

class BugReport(BaseModel):   # inherit from BaseModel = Pydantic model
    title: str = Field(min_length=3, max_length=200)   # Field adds validation rules
    description: str = Field(min_length=10)   # description must be at least 10 chars
    severity: Literal['low','medium','high','critical']   # only these 4 values
    reporter: str
    created_at: datetime = Field(default_factory=datetime.now)   # auto-set
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))   # auto-generate unique ID

    @field_validator('title')   # custom validator
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == '':
            raise ValueError('Title cannot be empty or just spaces')
        return v.strip()

class TriageResult(BaseModel):
    bug_id: str
    suggested_severity: Literal['low','medium','high','critical']
    category: str
    suggested_assignee: Optional[str] = None
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0)   # ge=greater or equal, le=less or equal

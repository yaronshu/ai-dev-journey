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


class Defect(BaseModel):   # how a stored defect (one DB row) is returned by the API
    id: str
    title: str
    description: str
    severity: str
    reporter: str
    status: Literal['open','in_progress','resolved','closed']
    created_at: datetime
    category: Optional[str] = None
    suggested_severity: Optional[str] = None
    suggested_assignee: Optional[str] = None
    explanation: Optional[str] = None
    confidence: Optional[float] = None


class DefectUpdate(BaseModel):   # PUT body — every field optional; send only what changes
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Literal['low','medium','high','critical']] = None
    status: Optional[Literal['open','in_progress','resolved','closed']] = None
    category: Optional[str] = None
    suggested_assignee: Optional[str] = None

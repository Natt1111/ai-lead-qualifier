from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class LeadScore(str, Enum):
    hot = "Hot"
    warm = "Warm"
    cold = "Cold"


class LeadSubmission(BaseModel):
    """Incoming lead data from the submission form."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    company: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)


class QualificationResult(BaseModel):
    """AI qualification output returned to the caller."""

    lead_score: int = Field(..., ge=0, le=100)
    score: LeadScore
    summary: str
    email_draft: str


class LeadRecord(LeadSubmission):
    """Full lead record stored in Airtable."""

    lead_score: Optional[int] = None
    score: Optional[LeadScore] = None
    summary: Optional[str] = None
    email_draft: Optional[str] = None
    airtable_id: Optional[str] = None

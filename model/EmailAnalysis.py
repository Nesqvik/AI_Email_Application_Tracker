from pydantic import BaseModel
from typing import Literal


class EmailAnalysis(BaseModel):
    is_job_related: bool

    category: Literal[
        "interview_invitation",
        "interview_followup",
        "rejection",
        "offer",
        "application_received",
        "assessment",
        "networking",
        "other_job_related",
        "not_job_related"
    ]

    company: str
    date: str
    summary: str
    confidence: float        
    language: Literal["en", "de", "other"]
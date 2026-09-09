from pydantic import BaseModel
from typing import Literal


class EmailAnalysis(BaseModel):
    id: str
    is_job_related: bool
    category: str
    company: str
    summary: str
    confidence: float
    date: str
    response: str
    language: Literal["en", "de", "other"]

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
    
     

    
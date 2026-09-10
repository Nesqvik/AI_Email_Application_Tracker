from enum import StrEnum
from pydantic import BaseModel


class EmailCategory(StrEnum):
    INTERVIEW_INVITATION = "interview_invitation"
    INTERVIEW_FOLLOWUP = "interview_followup"
    REJECTION = "rejection"
    OFFER = "offer"
    APPLICATION_RECEIVED = "application_received"
    ASSESSMENT = "assessment"
    NETWORKING = "networking"
    OTHER_JOB_RELATED = "other_job_related"
    NOT_JOB_RELATED = "not_job_related"


class Language(StrEnum):
    EN = "en"
    DE = "de"
    OTHER = "other"


class EmailAnalysis(BaseModel):
    is_job_related: bool
    category: EmailCategory
    company: str
    date: str
    summary: str
    confidence: float
    language: Language
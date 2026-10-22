from typing import Literal
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    qualification: str
    field_of_study: str
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    professional_registrations: list[str] = Field(
        default_factory=list
    )


class JobMatchRequest(BaseModel):
    candidate: CandidateProfile
    job_description: str = Field(min_length=10)


class RequirementAssessment(BaseModel):
    requirement: str
    mandatory: bool
    status: Literal["supported", "uncertain", "not_met"]
    job_evidence: str
    candidate_evidence: str
    explanation: str


class JobMatchResult(BaseModel):
    job_title: str
    recommendation: Literal[
        "potential_match",
        "review_required",
        "requirements_conflict"
    ]
    requirements: list[RequirementAssessment]
    summary: str
    next_action: str



class AgentSearchRequest(BaseModel):
    message: str = Field(
        min_length=3,
        max_length=500
    )
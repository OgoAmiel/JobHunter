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

    category: Literal[
        "mandatory",
        "preferred",
        "responsibility",
        "unspecified",
    ]

    status: Literal[
        "supported",
        "uncertain",
        "not_met",
    ]

    job_evidence: str
    candidate_evidence: str
    explanation: str


class JobResponsibility(BaseModel):
    description: str
    job_evidence: str

class LearningOpportunity(BaseModel):
    description: str
    job_evidence: str


class JobMatchResult(BaseModel):
    job_title: str
    recommendation: Literal[
        "potential_match",
        "review_required",
        "requirements_conflict",
    ]

    # Candidate selection requirements
    requirements: list[RequirementAssessment] = Field(
        default_factory=list
    )

    # Tasks performed in the position
    responsibilities: list[JobResponsibility] = Field(
        default_factory=list
    )

    # Skills and experience offered by the employer
    learning_opportunities: list[LearningOpportunity] = Field(
        default_factory=list
    )

    summary: str
    next_action: str

    validation_warnings: list[str] = Field(
        default_factory=list
    )

    unverified_requirements: list[
        RequirementAssessment
    ] = Field(default_factory=list)

    unverified_responsibilities: list[
        JobResponsibility
        ] = Field(default_factory=list)

    unverified_learning_opportunities: list[
        LearningOpportunity
        ] = Field(default_factory=list)


class AgentSearchRequest(BaseModel):
    message: str = Field(
        min_length=3,
        max_length=500
    )


class SearchAndMatchRequest(BaseModel):
    candidate: CandidateProfile
    keyword: str = Field(min_length=2, max_length=100)
    location: str = Field(
        default="Johannesburg",
        min_length=2,
        max_length=100,
    )


class JobListing(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str


class MatchedJob(BaseModel):
    job: JobListing
    evaluation: JobMatchResult | None = None
    assessment_note: str | None = None


class SearchAndMatchResponse(BaseModel):
    results: list[MatchedJob] = Field(default_factory=list)
    message: str | None = None
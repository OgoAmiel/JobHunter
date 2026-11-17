
from app.schemas import (
    JobMatchResult,
    RequirementAssessment,
)
from app.services.match_validation import validate_match_result


def create_assessment(requirement, evidence):
    return RequirementAssessment(
        requirement=requirement,
        category="responsibility",
        status="supported",
        job_evidence=evidence,
        candidate_evidence="Financial Reporting",
        explanation="Test assessment",
    )


def create_result(requirements):
    return JobMatchResult(
        job_title="Graduate Accountant",
        recommendation="potential_match",
        requirements=requirements,
        summary="Preliminary evaluation",
        next_action="Review the advertisement",
    )


def test_valid_evidence_is_preserved():
    description = (
        "You will work closely with senior "
        "accountants and auditors."
    )

    result = create_result([
        create_assessment(
            "work closely with senior accountants",
            "Work closely with senior accountants",
        )
    ])

    validated = validate_match_result(result, description)

    assert len(validated.requirements) == 1

    assert (
        validated.requirements[0].job_evidence
        == "work closely with senior accountants"
    )

    assert validated.unverified_requirements == []


def test_unverified_evidence_is_retained_separately():
    description = "Assist with bookkeeping."

    result = create_result([
        create_assessment(
            "Three years of accounting experience",
            "Three years of accounting experience",
        )
    ])

    validated = validate_match_result(result, description)

    assert validated.requirements == []
    assert len(validated.unverified_requirements) == 1

    assert (
        validated.unverified_requirements[0].status
        == "uncertain"
    )

    assert validated.recommendation == "review_required"


def test_truncated_description_requires_review():
    description = (
        "Assist with bookkeeping and financial rep…"
    )

    result = create_result([])

    validated = validate_match_result(result, description)

    assert validated.recommendation == "review_required"
    assert len(validated.validation_warnings) == 1
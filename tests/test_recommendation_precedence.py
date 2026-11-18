
from app.schemas import (
    JobMatchResult,
    RequirementAssessment,
)
from app.services.match_validation import validate_match_result


def test_mandatory_conflict_is_not_hidden_by_truncation():
    description = (
        "Applicants must hold a valid professional "
        "registration. Further details…"
    )

    result = JobMatchResult(
        job_title="Graduate Professional",
        recommendation="requirements_conflict",
        requirements=[
            RequirementAssessment(
                requirement="Valid professional registration",
                category="mandatory",
                status="not_met",
                job_evidence=(
                    "Applicants must hold a valid "
                    "professional registration"
                ),
                candidate_evidence=(
                    "Candidate explicitly confirms "
                    "they do not hold registration."
                ),
                explanation=(
                    "The candidate has confirmed "
                    "they do not satisfy this requirement."
                ),
            )
        ],
        summary="A mandatory requirement is not met.",
        next_action="Verify registration eligibility.",
    )

    validated = validate_match_result(
        result,
        description,
    )

    assert validated.recommendation == "requirements_conflict"
    assert len(validated.requirements) == 1
    assert validated.validation_warnings
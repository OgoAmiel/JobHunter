
from app.schemas import (
    JobMatchResult,
    RequirementAssessment,
)
from app.services.match_validation import validate_match_result


def test_fabricated_evidence_is_not_accepted():
    """
    A requirement must not pass validation merely
    because its name appears in the job advertisement.
    """

    description = (
        "Python knowledge is advantageous."
    )

    result = JobMatchResult(
        job_title="Graduate Developer",
        recommendation="potential_match",
        requirements=[
            RequirementAssessment(
                requirement="Python",
                category="mandatory",
                status="supported",
                job_evidence=(
                    "Candidates must have five years "
                    "of Python experience."
                ),
                candidate_evidence="Python",
                explanation="Candidate has Python skills.",
            )
        ],
        summary="Candidate appears suitable.",
        next_action="Consider applying.",
    )

    validated = validate_match_result(
        result,
        description,
    )

    assert validated.requirements == []

    assert len(
        validated.unverified_requirements
    ) == 1

    assert (
        validated.unverified_requirements[0].status
        == "uncertain"
    )

    assert validated.recommendation == "review_required"

    assert validated.validation_warnings

from app.schemas import (
    JobMatchResult,
    JobResponsibility,
    LearningOpportunity,
)
from app.services.match_validation import validate_match_result


def make_result(
    responsibilities=None,
    learning_opportunities=None,
):
    return JobMatchResult(
        job_title="Graduate Accountant",
        recommendation="potential_match",
        requirements=[],
        responsibilities=responsibilities or [],
        learning_opportunities=learning_opportunities or [],
        summary="Test evaluation",
        next_action="Review the advertisement",
    )


def test_valid_responsibility_is_preserved():
    description = (
        "You will work closely with senior "
        "accountants and auditors, learning new skills."
    )

    result = make_result(
        responsibilities=[
            JobResponsibility(
                description="Work with senior accountants",
                job_evidence=(
                    '"You will work closely with senior '
                    'accountants and auditors,"'
                ),
            )
        ]
    )

    validated = validate_match_result(result, description)

    assert len(validated.responsibilities) == 1
    assert validated.unverified_responsibilities == []
    assert validated.responsibilities[0].job_evidence == (
        "You will work closely with senior "
        "accountants and auditors,"
    )


def test_truncated_responsibility_is_excluded():
    description = (
        "Contributing to the financial integrity "
        "of our cli…"
    )

    result = make_result(
        responsibilities=[
            JobResponsibility(
                description="Financial integrity of clients",
                job_evidence=(
                    "Contributing to the financial "
                    "integrity of our cli…"
                ),
            )
        ]
    )

    validated = validate_match_result(result, description)

    assert validated.responsibilities == []
    assert len(validated.unverified_responsibilities) == 1
    assert validated.recommendation == "review_required"


def test_invented_learning_opportunity_is_excluded():
    description = "The role offers bookkeeping training."

    result = make_result(
        learning_opportunities=[
            LearningOpportunity(
                description="Advanced Python training",
                job_evidence="Advanced Python training",
            )
        ]
    )

    validated = validate_match_result(result, description)

    assert validated.learning_opportunities == []
    assert len(validated.unverified_learning_opportunities) == 1
    assert validated.recommendation == "review_required"
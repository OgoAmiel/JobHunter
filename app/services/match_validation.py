
import re

from app.schemas import JobMatchResult


def find_source_quote(
    quote: str,
    description: str,
) -> str | None:
    """
    Find a quotation in the original job advertisement.

    Matching ignores case and differences in whitespace.
    Surrounding quotation marks added by the AI are removed.

    Returns the matching text from the original description
    or None if the quotation cannot be verified.
    """

    quote = quote.strip().strip("\"'“”").strip()

    if not quote or quote.endswith(("...", "…")):
        return None

    pattern = r"\s+".join(
        re.escape(word) for word in quote.split()
    )

    match = re.search(
        pattern,
        description,
        flags=re.IGNORECASE,
    )

    return match.group(0) if match else None


def is_valid_source_quote(
    quote: str,
    description: str,
) -> bool:
    """
    Return True if the quotation can be found
    in the original job advertisement.
    """

    return find_source_quote(
        quote,
        description,
    ) is not None


def validate_match_result(
    result: JobMatchResult,
    source_description: str,
) -> JobMatchResult:
    """
    Validate AI-generated assessments against
    the original job advertisement.

    Checks evidence for:
    1. Candidate requirements.
    2. Job responsibilities.
    3. Learning opportunities.

    Unverified assessments are retained separately.

    A review is required whenever evidence cannot
    be verified or the advertisement is truncated.
    """

    validated = result.model_copy(deep=True)
    warnings: list[str] = []

    # ==========================================
    # 1. VALIDATE CANDIDATE REQUIREMENTS
    # ==========================================

    verified_requirements = []
    unverified_requirements = []

    for item in validated.requirements:
        evidence = find_source_quote(
            item.job_evidence,
            source_description,
        )

        if evidence is not None:
            item.job_evidence = evidence
            verified_requirements.append(item)

        else:
            item.status = "uncertain"
            unverified_requirements.append(item)

            warnings.append(
                f"Unverified requirement: {item.requirement}"
            )

    # ==========================================
    # 2. VALIDATE JOB RESPONSIBILITIES
    # ==========================================

    verified_responsibilities = []
    unverified_responsibilities = []

    for item in validated.responsibilities:
        evidence = find_source_quote(
            item.job_evidence,
            source_description,
        )

        if evidence is not None:
            item.job_evidence = evidence
            verified_responsibilities.append(item)

        else:
            unverified_responsibilities.append(item)

            warnings.append(
                f"Unverified responsibility: {item.description}"
            )

    # ==========================================
    # 3. VALIDATE LEARNING OPPORTUNITIES
    # ==========================================

    verified_learning = []
    unverified_learning = []

    for item in validated.learning_opportunities:
        evidence = find_source_quote(
            item.job_evidence,
            source_description,
        )

        if evidence is not None:
            item.job_evidence = evidence
            verified_learning.append(item)

        else:
            unverified_learning.append(item)

            warnings.append(
                "Unverified learning opportunity: "
                f"{item.description}"
            )

    # ==========================================
    # 4. CHECK FOR TRUNCATED ADVERTISEMENTS
    # ==========================================

    if source_description.rstrip().endswith(("...", "…")):
        warnings.append(
            "The job description appears to be truncated."
        )

    # ==========================================
    # 5. STORE VALIDATED RESULTS
    # ==========================================

    validated.requirements = verified_requirements
    validated.unverified_requirements = (
        unverified_requirements
    )

    validated.responsibilities = verified_responsibilities
    validated.unverified_responsibilities = (
        unverified_responsibilities
    )

    validated.learning_opportunities = verified_learning
    validated.unverified_learning_opportunities = (
        unverified_learning
    )

    validated.validation_warnings = warnings

    # ==========================================
    # 6. UPDATE OVERALL RECOMMENDATION
    # ==========================================

    has_mandatory_conflict = any(
    item.category == "mandatory"
    and item.status == "not_met"
    for item in validated.requirements
)
    if has_mandatory_conflict:
        validated.recommendation = "requirements_conflict"

    elif warnings:
        validated.recommendation = "review_required"

    return validated
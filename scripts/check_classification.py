from app.agent import evaluate_job
from app.schemas import CandidateProfile


candidate = CandidateProfile(
    qualification="BCom Accounting",
    field_of_study="Accounting",
    skills=["Microsoft Excel", "Bookkeeping"],
    experience=[],
)

advertisement = """
Job Title: Graduate Accountant

Applicants must hold a BCom Accounting degree.

Microsoft Excel experience is preferred.

You will prepare monthly bank reconciliations.

Training in tax preparation will be provided.
"""


def main():
    result = evaluate_job(
        candidate=candidate,
        job_description=advertisement,
        source_description=advertisement,
    )

    print("\n=== REQUIREMENTS ===")

    for item in result.requirements:
        print(
            f"[{item.category}] "
            f"{item.requirement}"
        )

    print("\n=== RESPONSIBILITIES ===")

    for item in result.responsibilities:
        print(item.description)

    print("\n=== LEARNING OPPORTUNITIES ===")

    for item in result.learning_opportunities:
        print(item.description)

    print("\n=== RECOMMENDATION ===")
    print(result.recommendation)

    checks = {
        "BCom is mandatory": any(
            item.category == "mandatory"
            and "bcom" in item.job_evidence.lower()
            for item in result.requirements
        ),
        "Excel is preferred": any(
            item.category == "preferred"
            and "excel" in item.job_evidence.lower()
            for item in result.requirements
        ),
        "Reconciliations are a responsibility": any(
            "reconciliation" in item.job_evidence.lower()
            for item in result.responsibilities
        ),
        "Tax training is a learning opportunity": any(
            "tax preparation" in item.job_evidence.lower()
            for item in result.learning_opportunities
        ),
    }

    print("\n=== CLASSIFICATION CHECKS ===")

    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")

    if not all(checks.values()):
        raise SystemExit(
            "Classification check failed. Review the output."
        )


if __name__ == "__main__":
    main()
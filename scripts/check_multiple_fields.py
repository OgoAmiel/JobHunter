from app.agent import evaluate_job
from app.schemas import CandidateProfile


CASES = [
    {
        "name": "Software Development",
        "candidate": CandidateProfile(
            qualification="BSc in Information Technology",
            field_of_study="Information Technology",
            skills=["Python", "REST APIs"],
            experience=[],
        ),
        "advertisement": """
Job Title: Graduate Backend Developer

Applicants must hold a BSc in Information Technology.

Docker experience is preferred.

You will develop and test REST APIs.

Training in AWS cloud deployment will be provided.
""",
        "expected": [
            ("requirements", "mandatory", "Information Technology"),
            ("requirements", "preferred", "Docker"),
            ("responsibilities", None, "REST APIs"),
            ("learning_opportunities", None, "AWS cloud deployment"),
        ],
        "not_expected": [
            ("responsibilities", "AWS cloud deployment"),
        ],
    },
    {
        "name": "Civil Engineering",
        "candidate": CandidateProfile(
            qualification="BEng in Civil Engineering",
            field_of_study="Civil Engineering",
            skills=["AutoCAD"],
            experience=[],
        ),
        "advertisement": """
Job Title: Graduate Civil Engineer

Candidates must hold a BEng in Civil Engineering.

GIS experience is advantageous.

You will assist with site inspections.

Mentorship in structural design will be provided.
""",
        "expected": [
            ("requirements", "mandatory", "Civil Engineering"),
            ("requirements", "preferred", "GIS"),
            ("responsibilities", None, "site inspections"),
            ("learning_opportunities", None, "structural design"),
        ],
        "not_expected": [
            ("responsibilities", "structural design"),
        ],
    },
]


def contains_evidence(result, section, text, category=None):
    items = getattr(result, section)

    return any(
        text.lower() in item.job_evidence.lower()
        and (
            category is None
            or item.category == category
        )
        for item in items
    )


def main():
    failures = 0

    for case in CASES:
        print(f"\n=== {case['name']} ===")

        result = evaluate_job(
            candidate=case["candidate"],
            job_description=case["advertisement"],
            source_description=case["advertisement"],
        )

        print("Recommendation:", result.recommendation)

        case_failed = False

        for section, category, text in case["expected"]:
            passed = contains_evidence(
                result, section, text, category
            )

            print(
                f"{'PASS' if passed else 'FAIL'}: "
                f"{section} / {text}"
            )

            if not passed:
                failures += 1
                case_failed = True

        for section, text in case["not_expected"]:
            passed = not contains_evidence(
                result, section, text
            )

            print(
                f"{'PASS' if passed else 'FAIL'}: "
                f"{text} excluded from {section}"
            )

            if not passed:
                failures += 1
                case_failed = True

        if case_failed:
            print("\nFull evaluation for debugging:")
            print(result.model_dump_json(indent=2))

    print(f"\nTotal failed checks: {failures}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
from app.agent import evaluate_job
from app.schemas import CandidateProfile


ADVERTISEMENT = """
Job Title: Graduate Civil Engineer

Applicants must be registered with ECSA.

You will assist engineers with site inspections.
"""


CASES = [
    {
        "name": "Registration information missing",
        "registrations": None,
        "expected_status": "uncertain",
        "expected_recommendation": "review_required",
    },
    {
        "name": "Registration explicitly not held",
        "registrations": [],
        "expected_status": "not_met",
        "expected_recommendation": "requirements_conflict",
    },
]


def main():
    failures = 0

    for case in CASES:
        print(f"\n=== {case['name']} ===")

        candidate = CandidateProfile(
            qualification="BEng Civil Engineering",
            field_of_study="Civil Engineering",
            skills=["AutoCAD"],
            experience=[],
            professional_registrations=case["registrations"],
        )

        result = evaluate_job(
            candidate=candidate,
            job_description=ADVERTISEMENT,
            source_description=ADVERTISEMENT,
        )

        matching = [
            item
            for item in result.requirements
            if item.category == "mandatory"
            and "ecsa" in item.job_evidence.lower()
        ]

        actual_status = (
            matching[0].status
            if matching
            else "missing"
        )

        status_passed = (
            actual_status == case["expected_status"]
        )

        recommendation_passed = (
            result.recommendation
            == case["expected_recommendation"]
        )

        print("Requirement status:", actual_status)
        print("Recommendation:", result.recommendation)

        print(
            "PASS" if status_passed else "FAIL",
            "- Requirement status",
        )

        print(
            "PASS" if recommendation_passed else "FAIL",
            "- Recommendation",
        )

        if not status_passed or not recommendation_passed:
            failures += 1
            print(result.model_dump_json(indent=2))

    print(f"\nFailed scenarios: {failures}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
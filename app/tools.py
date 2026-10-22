import json
import re

from agents import function_tool


SAMPLE_JOBS = [
    {
        "id": "demo-001",
        "title": "Graduate Finance Assistant",
        "field": "Accounting",
        "location": "Johannesburg",
        "description": "BCom Accounting, Excel and financial reporting.",
    },
    {
        "id": "demo-002",
        "title": "Graduate Software Developer",
        "field": "Software Engineering",
        "location": "Pretoria",
        "description": "Python, SQL and REST API knowledge.",
    },
    {
        "id": "demo-003",
        "title": "Graduate Marketing Assistant",
        "field": "Marketing",
        "location": "Johannesburg",
        "description": "Marketing qualification, communication and social media.",
    },
]


def find_demo_jobs(keyword: str) -> list[dict]:
    """Find sample jobs using meaningful search terms."""

    stop_words = {
        "find", "search", "me", "for", "in",
        "jobs", "job", "roles", "role",
        "positions", "position", "the", "a",
        "please",
    }

    words = set(re.findall(r"[a-z0-9]+", keyword.lower()))

    search_terms = words - stop_words

    if not search_terms:
        return []

    matches = []

    for job in SAMPLE_JOBS:
        searchable_text = " ".join([
            job["title"],
            job["field"],
            job["location"],
            job["description"],
        ]).lower()

        job_words = set(
            re.findall(r"[a-z0-9]+", searchable_text)
        )

        if search_terms.issubset(job_words):
            matches.append(job)

    return matches


@function_tool
def search_demo_jobs(keyword: str) -> str:
    """Search fictional graduate jobs by keyword."""

    matches = find_demo_jobs(keyword)

    return json.dumps({
        "source": "fictional_demo_data",
        "count": len(matches),
        "jobs": matches,
    })

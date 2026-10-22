import os

import httpx
from dotenv import load_dotenv

load_dotenv()


async def search_jobs(
    keyword: str,
    location: str = "Johannesburg",
    limit: int = 5,
) -> list[dict]:

    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError("Missing Adzuna API credentials")

    url = "https://api.adzuna.com/v1/api/jobs/za/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": keyword,
        "where": location,
        "results_per_page": limit,
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Adzuna returned HTTP {exc.response.status_code}"
        ) from None
    except httpx.RequestError:
        raise RuntimeError("Could not connect to Adzuna") from None

    data = response.json()
    jobs = []

    for item in data.get("results", []):
        jobs.append({
            "id": str(item.get("id", "")),
            "title": item.get("title", ""),
            "company": (item.get("company") or {}).get(
                "display_name", "Unknown"
            ),
            "location": (item.get("location") or {}).get(
                "display_name", "Unknown"
            ),
            "description": item.get("description", ""),
            "url": item.get("redirect_url", ""),
            "source": "Adzuna",
        })

    return jobs
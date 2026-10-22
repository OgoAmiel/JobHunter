import asyncio
import httpx
from app.services import adzuna


def test_adzuna_search_returns_jobs(monkeypatch):
    # Use fictional credentials for testing
    monkeypatch.setenv("ADZUNA_APP_ID", "test-id")
    monkeypatch.setenv("ADZUNA_APP_KEY", "test-key")

    # Simulate the Adzuna response
    def mock_response(request):
        assert request.url.params["what"] == "graduate"

        return httpx.Response(
            200,
            json={
                "count": 1,
                "results": [
                    {
                        "id": "123",
                        "title": "Graduate Accountant",
                        "company": {
                            "display_name": "Example Company"
                        },
                        "location": {
                            "display_name": "Johannesburg"
                        },
                        "description": "Accounting graduate role",
                        "redirect_url": "https://example.com/job",
                    }
                ],
            },
        )

    transport = httpx.MockTransport(mock_response)
    original_client = httpx.AsyncClient

    def mock_client(*args, **kwargs):
        return original_client(
            *args,
            transport=transport,
            **kwargs,
        )

    monkeypatch.setattr(
        adzuna.httpx,
        "AsyncClient",
        mock_client,
    )

    jobs = asyncio.run(
        adzuna.search_jobs("graduate", "Johannesburg")
    )

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Graduate Accountant"
    assert jobs[0]["company"] == "Example Company"
    assert jobs[0]["source"] == "Adzuna"

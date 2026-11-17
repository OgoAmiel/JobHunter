from fastapi import FastAPI
from agents import Runner

import asyncio

from app.agent import evaluate_job, job_search_agent, real_job_search_agent
from app.services.adzuna import search_jobs

from app.schemas import (
    JobMatchRequest,
    JobMatchResult,
    AgentSearchRequest,
    SearchAndMatchRequest,
    SearchAndMatchResponse,
    JobListing,
    MatchedJob,
)


app = FastAPI(
    title="JobHunter AI",
    description="AI-powered job matching for South African graduates",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/match", response_model=JobMatchResult)
def match_job(request: JobMatchRequest):
    return evaluate_job(
        candidate=request.candidate,
        job_description=request.job_description,
    )


@app.post("/agent/demo-search")
async def agent_demo_search(request: AgentSearchRequest):

    result = await Runner.run(
        job_search_agent,
        request.message,
        max_turns=5,
    )

    return {
        "response": result.final_output
    }


@app.post("/agent/search")
async def search_real_jobs(request: AgentSearchRequest):

    result = await Runner.run(
        real_job_search_agent,
        request.message,
        max_turns=5,
    )

    return {
        "response": result.final_output
    }



@app.post(
    "/jobs/search-and-match",
    response_model=SearchAndMatchResponse,
)
async def search_and_match(request: SearchAndMatchRequest):

    # 1. Fetch a real job from Adzuna
    jobs = await search_jobs(
        keyword=request.keyword,
        location=request.location,
        limit=1,
    )

    # 2. Handle empty search results
    if not jobs:
        return SearchAndMatchResponse(
            results=[],
            message="No matching jobs were found.",
        )

    # 3. Validate the returned job data
    job = JobListing.model_validate(jobs[0])

    # 4. Avoid analysing an empty description
    if not job.description.strip():
        return SearchAndMatchResponse(
            results=[
                MatchedJob(
                    job=job,
                    assessment_note=(
                        "No job description was available. "
                        "Eligibility was not assessed."
                    ),
                )
            ],
            message="Job found, but analysis was skipped.",
        )

    # 5. Prepare the job advertisement for OpenAI
    description = (
        f"Job title: {job.title}\n"
        f"Location: {job.location}\n"
        "The following advertisement excerpt may be incomplete. "
        "Do not infer unstated requirements.\n\n"
        f"Description:\n{job.description}"
    )

    # 6. Evaluate the candidate using OpenAI
    evaluation = await asyncio.to_thread(
        evaluate_job,
        request.candidate,
        description,
        job.description,
        )

    # 7. Return the original job and AI assessment
    return SearchAndMatchResponse(
        results=[
            MatchedJob(
                job=job,
                evaluation=evaluation,
                assessment_note=(
                    "Preliminary assessment based on "
                    "Adzuna's available description. "
                    "Verify requirements and availability "
                    "on the original listing."
                ),
            )
        ],
        message="One job retrieved and evaluated.",
    )
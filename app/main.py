from fastapi import FastAPI
from agents import Runner

from app.agent import evaluate_job, job_search_agent
from app.schemas import (
    JobMatchRequest,
    JobMatchResult,
    AgentSearchRequest,
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

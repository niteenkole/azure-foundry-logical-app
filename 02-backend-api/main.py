# Read configuration from the backend process environment; secrets stay out of source code.
import os
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from sys import path as sys_path

sys_path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../03-policy")))
from guardrails import validate_question
sys_path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../04-foundry")))
from client import FoundryConfigurationError, FoundryRequestError, complete_chat
sys_path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../05-controls")))
from telemetry import record_call, record_failure, start_trace

# Load the backend folder's .env for local development; secrets remain server-side.
load_dotenv(Path(__file__).with_name(".env"))

# Create the HTTP API that the browser will call instead of calling Foundry directly.
app = FastAPI(title="Enterprise Policy Assistant API")

# Allow the local frontend to call this API during the demo.
# In production, replace the wildcard with the exact approved frontend origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class AskRequest(BaseModel):
    # Validate the incoming question before it reaches the model.
    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    # Keep the response contract simple and predictable for the frontend.
    answer: str


@app.get("/health")
def health() -> dict[str, str]:
    # Give the frontend or operator a cheap way to confirm that the API process is alive.
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    # Apply the shared policy module before selecting a model or making a network call.
    try:
        question = validate_question(request.question)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    # Create a trace ID and timer without storing the user's prompt in logs.
    trace_id, started_at = start_trace()
    model_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT") or os.environ.get(
        "MODEL_DEPLOYMENT", "configured-deployment"
    )
    try:
        # The Foundry module owns deployment selection, authentication, and the SDK call.
        answer = complete_chat(question)
        # Record only operational metadata: trace ID, deployment name, and latency.
        record_call(trace_id, model_name, started_at)
        return AskResponse(answer=answer)
    except FoundryConfigurationError as error:
        # Configuration problems are reported separately from provider failures.
        record_failure(trace_id, model_name, started_at)
        raise HTTPException(status_code=503, detail=str(error)) from error
    except FoundryRequestError as error:
        # Do not expose credentials or provider details to the browser; log safely server-side.
        record_failure(trace_id, model_name, started_at)
        raise HTTPException(status_code=502, detail=str(error)) from error

"""
Minimal Langchain service using FastAPI and Pydantic.

Includes endpoints to retrieve, update and create agents.

Attributes:
    app (FastAPI): The instance of the FastAPI framework.
"""

from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import Agent

load_dotenv()

app = FastAPI()

agent = Agent()


class Query(BaseModel):
    """Query model."""

    query: str


@app.get("/")
def read_root() -> Any:
    """Returns a greeting message."""
    return {"message": "Welcome to langchain service!"}


@app.post("/qa")
def qa(query: Query):
    """Run the agent on a query"""
    response = agent.run(query.query)
    return {"response": response}

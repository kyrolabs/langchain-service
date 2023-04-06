"""
Minimal Langchain service using FastAPI and Pydantic.

Includes endpoints to retrieve, update and create agents.

Attributes:
    app (FastAPI): The instance of the FastAPI framework.
"""

from typing import Any, Optional

from agent import Agent
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root() -> Any:
    """Returns a greeting message."""
    return {"message": "Welcome to langchain service!"}


@app.get("/agents/{agent_id}")
def read_agent(agent_id: int, query: Optional[str]):
    """Retrieve information for specific agent by their ID."""
    return {"agent_id": agent_id, "query": query}


@app.put("/agents/{agent_id}")
def update_agent(agent_id: int, agent: Agent):
    """Update an existing agent with a new name."""
    return {"agent_name": agent.name, "agent_id": agent_id}


@app.post("/data")
def ingest_data(data: str):
    """Ingest data to the database and process its embeddings."""
    return {"data": data}

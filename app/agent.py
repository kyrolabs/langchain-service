""""Agent model."""

# from langchain.models import Agent

from pydantic import BaseModel

class Agent(BaseModel):
    """Agent model."""
    name: str

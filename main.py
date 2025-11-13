from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.models.google import Gemini
from agno.knowledge.embedder.google import GeminiEmbedder
from train import bugReportknowledgeBase
from pydantic import BaseModel, Field
import pandas as pd
import os

def similaritySearchAgent(bug):
    knowledge = Knowledge(
            vector_db=ChromaDb(
                collection="csv_data",
                path="bugKB/chromadb",
                embedder=GeminiEmbedder(api_key="AIzaSyB7S3bAMC49oCDocCzIyOaDuEm-q8Gm8t0"),
                persistent_client=True
            ),

        )
    agent = Agent(
                model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
                knowledge=knowledge,
                search_knowledge=True,
                instructions=[
                    "Search the knowledge base for similar bug_descriptions, the descriptions might have a different tone, but if the meaning or the error they are pointing to is same, mark them as SIMILAR",
                    "If found, return the similar query and set similarity_status to 'Similar query found'.",
                    "If not found, set similarity_status to 'Unique query'.",
                    "Always assign a priority: high, medium, or low based on severity.",
                    "Your output should be of this format - similarity_status: unique/similar, priority: high/medium/low"
                ],
                markdown=True,
                # output_schema=BugReport,

            )

    response = agent.run(f"Search for this bug description in the knowledge base: {bug}")
    text = response.content
    print(text)
    result = {}

    for line in text.splitlines():
        if ":" in line:  # ignore lines without key-value pairs
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()

    return result

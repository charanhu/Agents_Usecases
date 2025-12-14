"""Academic_websearch_agent for finding research papers using search tools."""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

from google.adk.models.lite_llm import LiteLlm

import os
from dotenv import load_dotenv

load_dotenv()

# model = LiteLlm(model=os.getenv("GROQ_MODEL"))

model = os.getenv("GOOGLE_MODEL_NAME")

academic_websearch_agent = Agent(
    model=model,
    name="academic_websearch_agent",
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
    output_key="recent_citing_papers",
    tools=[google_search],
)
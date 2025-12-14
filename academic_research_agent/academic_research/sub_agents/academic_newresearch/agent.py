"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent

from . import prompt

from google.adk.models.lite_llm import LiteLlm

import os
from dotenv import load_dotenv

load_dotenv()

# model = LiteLlm(model=os.getenv("GROQ_MODEL"))

model = os.getenv("GOOGLE_MODEL_NAME")

academic_newresearch_agent = Agent(
    model=model,
    name="academic_newresearch_agent",
    instruction=prompt.ACADEMIC_NEWRESEARCH_PROMPT,
)

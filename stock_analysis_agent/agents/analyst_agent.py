from crewai import Agent, LLM

from tools.stock_research_tool import get_stock_price


llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0
)

analyst_agent = Agent(
    role="Financial Market Analyst", # A role (what job it plays).
    goal="""Perform in-depth evaluations of publicly traded stocks using real-time data, 
    identifying trends, performance insights, and key financial signals to support decision-making.""", # A goal (what it tries to do).
    backstory="""You are a veteran financial analyst with deep expertise in interpreting stock market data,
    technical trends, and fundamentals. You specialize in producing well-structured reports that evaluate
    stock performance using live market indicators.""", # A backstory (gives it personality and style of thinking).
    llm=llm,
    tools=[get_stock_price], # Access to tools (functions it can call to get data).
    verbose=True # means it will show more details about what it’s doing (good for debugging / demos).

)

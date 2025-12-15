import datetime
from zoneinfo import ZoneInfo
from ddgs import DDGS
import arxiv  # Add this import
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv


load_dotenv()


llm = LiteLlm(model="groq/llama-3.3-70b-versatile")



def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }



def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}



def web_search(query: str, max_results: int = 5) -> dict:
    """Performs a web search using DuckDuckGo and returns the results.

    Args:
        query (str): The search query string.
        max_results (int, optional): Maximum number of results to return. Defaults to 5.

    Returns:
        dict: status and search results or error msg.
    """
    try:
        results = DDGS().text(query, max_results=max_results)

        # Format results into a readable structure
        search_results = []
        for result in results:
            search_results.append(
                {
                    "title": result.get("title", "No title"),
                    "url": result.get("href", "No URL"),
                    "description": result.get("body", "No description"),
                }
            )

        if search_results:
            return {
                "status": "success",
                "query": query,
                "results": search_results,
                "count": len(search_results),
            }
        else:
            return {
                "status": "error",
                "error_message": f"No results found for query: '{query}'",
            }

    except Exception as e:
        return {"status": "error", "error_message": f"Search failed: {str(e)}"}



def search_arxiv(query: str, max_results: int = 5) -> dict:
    """Searches arXiv for academic papers and returns the results.

    Args:
        query (str): The search query string (can include author, title, abstract keywords).
        max_results (int, optional): Maximum number of results to return. Defaults to 5.

    Returns:
        dict: status and search results or error msg.
    """
    try:
        # Create arXiv client
        client = arxiv.Client()

        # Construct search
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        # Fetch results
        results = client.results(search)

        # Format results into a readable structure
        paper_results = []
        for paper in results:
            paper_results.append(
                {
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary[:500] + "..." if len(paper.summary) > 500 else paper.summary,
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "url": paper.entry_id,
                    "pdf_url": paper.pdf_url,
                    "categories": paper.categories,
                }
            )

        if paper_results:
            return {
                "status": "success",
                "query": query,
                "results": paper_results,
                "count": len(paper_results),
            }
        else:
            return {
                "status": "error",
                "error_message": f"No papers found for query: '{query}'",
            }

    except Exception as e:
        return {"status": "error", "error_message": f"arXiv search failed: {str(e)}"}



root_agent = Agent(
    name="weather_time_search_agent",
    model=llm,
    description=(
        "Agent to answer questions about time, weather, perform web searches, and search academic papers."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city, "
        "perform web searches to find information on any topic, and search arXiv for academic papers and research."
    ),
    tools=[get_weather, get_current_time, web_search, search_arxiv],
)

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing import Dict
from graph.state import State
from model.llm import llm

load_dotenv(dotenv_path="./config/.env")

@tool
def search_tool(query: str) -> str:
    """Search the web for information."""
    search = TavilySearch(max_results=3)
    results = search.invoke(query)
    return str(results)

researcher_llm = llm.bind_tools([search_tool])

def researcher_agent(state: State) -> Dict:

    task = state.get("task", "")

    research_prompt = f"""As a research specialist, provide comprehensive using search_tool information about: {task}

    Include:
    1. Key facts and background
    2. Current trends or developments
    3. Important statistics or data points
    4. Notable examples or case studies
    
    Be concise but thorough."""

    response = researcher_llm.invoke([HumanMessage(content=research_prompt)])

    if "tool_calls" in response.additional_kwargs and response.additional_kwargs["tool_calls"]:
        tool_call = response.additional_kwargs["tool_calls"][0]

        args = tool_call["function"]["arguments"]

        tool_result = search_tool.invoke(args)

        followup = llm.invoke([
            HumanMessage(content=f"Here are the tool results:\n{tool_result}\n\nSummarize them into a clean research summary.")
        ])

        research_text = followup.content.strip()
    else:
        research_text = response.content.strip()


    return {
        "messages": [AIMessage(content="🔍 Research completed.")],
        "research_data": research_text,
        "next_agent": "supervisor"
    }
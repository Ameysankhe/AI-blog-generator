from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict
from graph.state import State
from model.llm import llm

def analyst_agent(state: State) -> Dict:

    research_data = state.get("research_data", "")
    task = state.get("task", "")

    analysis_prompt = f"""As a data analyst, analyze this research data and provide insights:

    Research Data:
    {research_data}

    Provide:
    1. Key insights and patterns
    2. Strategic implications
    3. Risks and opportunities
    4. Recommendations

    Focus on actionable insights related to: {task}"""

    analysis_response = llm.invoke([HumanMessage(content=analysis_prompt)])
    analysis = analysis_response.content

    return {
        "messages": [AIMessage(content="📊 Analysis completed.")],
        "analysis_data": analysis,
        "next_agent": "supervisor"
    }
from langchain_core.messages import AIMessage
from typing import Dict
from graph.state import State

def supervisor_agent(state: State) -> Dict:

    if not state.get("task"):
        task = state["messages"][-1].content
    else:
        task = state["task"]

    has_research = bool(state.get("research_data"))
    has_analysis = bool(state.get("analysis_data"))
    has_blog = bool(state.get("blog"))

    if not has_research:
        next_agent = "researcher"
        supervisor_msg = "📋 Starting research..."
    elif not has_analysis:
        next_agent = "analyst"
        supervisor_msg = "📊 Starting analysis..."
    elif not has_blog:
        next_agent = "writer"
        supervisor_msg = "✍️ Starting writing..."
    else:
        next_agent = "end"
        supervisor_msg = "🟢 Blog complete!"
    
    return {
        "messages": [AIMessage(content=supervisor_msg)],
        "next_agent": next_agent,
        "task": task,
        "task_complete": (next_agent == "end")
    }
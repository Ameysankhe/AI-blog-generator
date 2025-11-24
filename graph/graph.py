from langgraph.graph import StateGraph, END
from typing import Literal
from graph.state import State
from agents.researcher import researcher_agent
from agents.analyst import analyst_agent
from agents.writer import writer_agent
from agents.supervisor import supervisor_agent

def router(state: State) -> Literal["supervisor", "researcher", "analyst", "writer", "__end__"]:
    next_agent = state.get("next_agent", "supervisor")

    if state.get("task_complete"):
        return END

    return next_agent

def build_graph():
    workflow = StateGraph(State)
    
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("writer", writer_agent)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        router,
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            END: END
        }
    )

    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("analyst", "supervisor")
    workflow.add_edge("writer", "supervisor")

    return workflow.compile()

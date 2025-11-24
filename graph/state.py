from langgraph.graph import MessagesState

class State(MessagesState):
    next_agent: str = ""
    research_data: str = ""
    analysis_data: str = ""
    blog: str = ""
    task: str = ""
    tone: str = ""
    length: str = ""
    audience: str = ""
    task_complete: bool = False
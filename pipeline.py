import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph.graph import build_graph

load_dotenv(dotenv_path="./config/.env")

graph = build_graph()

def run_pipeline(topic: str, tone: str, length: str, audience: str):

    for event in graph.stream(
        {
            "messages": [HumanMessage(content=topic)],
            "tone": tone,
            "length": length,
            "audience": audience,
        },
        stream_mode="updates"
    ):
        yield event
        


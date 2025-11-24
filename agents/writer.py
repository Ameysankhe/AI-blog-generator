from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict
from graph.state import State
from model.llm import llm

def writer_agent(state: State) -> Dict:
    task = state.get("task", "")
    research_data = state.get("research_data", "")
    analysis_data = state.get("analysis_data", "")
    tone = state.get("tone", "professional")
    length = state.get("length", "medium")
    audience = state.get("audience", "general readers")

    writing_prompt = f"""
    You are a professional blog writer.

    Your task: Create a polished, engaging, well-structured blog based on the topic, 
    research, analysis, and filters below.

    --- USER FILTERS ---
    Tone: {tone}
    Length: {length}
    Target Audience: {audience}

    --- DATA ---
    Blog Topic: {task}

    Research Summary:
    {research_data[:1500]}

    Analyst Insights:
    {analysis_data[:1500]}

    --- STRICT OUTPUT FORMAT ---
    You MUST return the blog ONLY in this exact structure:

    **TITLE** 
    Write one compelling, SEO-friendly title. Bold using Markdown (**Title**).

    **Introduction**  
    Write exactly ONE paragraph of EXACTLY 5 lines.  
    Each line must be separated using a manual line break.  
    Each line must be a complete sentence.  
    NO extra lines.

    **Main Section**  
    Write 2 or 3 paragraphs.  
    Each paragraph must contain EXACTLY 6-7 lines.  
    Each line must be separated using a manual line break.  
    Paragraphs must be separated by one blank line.

    **Conclusion**  
    Write ONE paragraph of EXACTLY 3-4 lines.  
    Each line must be separated with a manual line break.

    --- RULES ---
    - Adapt tone based on user choice.
    - Adjust writing style to suit the target audience.
    - Expand or compress content depending on length setting (short, medium, long).
    - Use research data for accuracy.
    - Use analyst insights for clarity and interpretation.
    - No extra headings.
    - No bullets.
    - Do NOT exceed line limits.
    """

    blog_response = llm.invoke([HumanMessage(content=writing_prompt)])
    blog = blog_response.content

    final_blog = f"""{blog}"""

    return {
        "messages": [AIMessage(content="✍️ Blog writing complete.")],
        "blog": final_blog,
        "next_agent": "supervisor",
        "task_complete": True
    }

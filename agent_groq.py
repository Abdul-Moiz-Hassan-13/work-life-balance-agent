from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------
# 1. Define the State
# -----------------------------------------
class AgentState(TypedDict):
    user_prompt: str
    user_context: Optional[Dict[str, Any]]
    analysis: Optional[Dict[str, Any]]

# -----------------------------------------
# 2. System Prompt Template
# -----------------------------------------
SYSTEM_PROMPT = """
You are the Work-Life Balance Diagnostic Agent.

Your task is to analyze the user’s work habits, daily routine, and lifestyle patterns. 
You must produce a JSON object that strictly follows this schema:

{
  "balanced": boolean,
  "risk_level": "low" | "medium" | "high",
  "summary": "string",
  "signals": ["string"],
  "recommendations": [
    {
      "category": "string",
      "advice": "string",
      "priority": "low" | "medium" | "high"
    }
  ]
}

CRITICAL RULES:
- Output MUST be valid JSON.
- Do NOT include backticks.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT include text outside the JSON object.
- Use only the fields listed in the schema.
- Never wrap the JSON in quotes.
- Never respond with multiple JSON blocks.

Your entire response MUST be exactly one JSON object.
"""

# -----------------------------------------
# JSON Repair Helper
# -----------------------------------------
def repair_json(invalid_text: str) -> dict:
    import re

    try:
        match = re.search(r'\{.*\}', invalid_text, re.DOTALL)
        if match:
            cleaned = match.group(0)
            return json.loads(cleaned)
    except:
        pass

    return {
        "balanced": False,
        "risk_level": "medium",
        "summary": "We could not parse your routine cleanly.",
        "signals": ["Malformed JSON from model"],
        "recommendations": [
            {
                "category": "general",
                "advice": "Please describe your work hours, sleep schedule, breaks, and stress level more clearly.",
                "priority": "medium"
            }
        ]
    }

# -----------------------------------------
# 3. Node: Analyzer (Groq Version)
# -----------------------------------------
def work_life_balance_analyzer(state: AgentState) -> AgentState:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )

    user_prompt = state["user_prompt"]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    response = llm.invoke(messages)
    raw_output = response.content

    try:
        parsed = json.loads(raw_output)
    except Exception:
        parsed = repair_json(raw_output)

    state["analysis"] = parsed
    return state

# -----------------------------------------
# 4. Build the Graph
# -----------------------------------------
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("analyzer", work_life_balance_analyzer)
    graph.set_entry_point("analyzer")

    graph.add_edge("analyzer", END)

    return graph.compile()

agent_app = build_agent()

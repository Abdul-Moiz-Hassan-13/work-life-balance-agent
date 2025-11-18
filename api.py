from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum
from agent_groq import agent_app
import traceback

from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# 1. CREATE APP
# ============================================================
app = FastAPI(
    title="Work-Life Balance Agent API",
    description="HTTP API for evaluating user work-life balance",
    version="1.0"
)


# ============================================================
# 2. CORS MIDDLEWARE
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 3. REQUEST FORMAT (Supervisor → Agent)
# ============================================================

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    role: Role
    content: str


class AgentRequest(BaseModel):
    messages: List[Message]


# ============================================================
# 4. RESPONSE FORMAT (Agent → Supervisor)
# ============================================================

class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class AgentResponse(BaseModel):
    agent_name: str
    status: Status
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


# ============================================================
# 5. Health Check
# ============================================================

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ============================================================
# 6. ANALYZE ENDPOINT — MAIN ENTRY
# ============================================================
@app.post("/analyze", response_model=AgentResponse)
def analyze(request: AgentRequest):
    try:
        # Extract the latest user message
        user_messages = [m.content for m in request.messages if m.role == Role.USER]

        if not user_messages:
            return AgentResponse(
                agent_name="work-life-agent",
                status=Status.ERROR,
                data=None,
                error_message="No user message found in request."
            )

        latest_user_input = user_messages[-1]

        # Build LangGraph state
        state = {
            "user_prompt": latest_user_input,
            "user_context": None,
            "analysis": None
        }

        # Run your agent
        result = agent_app.invoke(state)

        # Extract analysis
        agent_output = result.get("analysis")

        # IMPORTANT FIX — wrap inside {"message": ...}
        return AgentResponse(
            agent_name="work-life-agent",
            status=Status.SUCCESS,
            data={"message": agent_output},
            error_message=None
        )

    except Exception as e:
        traceback.print_exc()

        return AgentResponse(
            agent_name="work-life-agent",
            status=Status.ERROR,
            data=None,
            error_message=str(e)
        )

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
# 2. CORS MIDDLEWARE - FIXED
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:3000",
        "https://work-life-balance-agent.netlify.app",
        "https://*.netlify.app",
        "*"  # Allow all origins for testing
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ============================================================
# 3. REQUEST FORMAT
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
# 4. RESPONSE FORMAT
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

@app.options("/health")
async def options_health():
    return {
        "message": "CORS preflight successful"
    }

# ============================================================
# 6. OPTIONS handler for analyze endpoint
# ============================================================
@app.options("/api/work-life-balance/analyze")
async def options_analyze():
    return {
        "message": "CORS preflight successful"
    }

# ============================================================
# 7. ANALYZE ENDPOINT — SIMPLIFIED ROUTE
# ============================================================
@app.post("/api/work-life-balance/analyze", response_model=AgentResponse)
def analyze(request: AgentRequest):
    try:
        user_messages = [m.content for m in request.messages if m.role == Role.USER]

        if not user_messages:
            return AgentResponse(
                agent_name="work-life-agent",
                status=Status.ERROR,
                data=None,
                error_message="No user message found in request."
            )

        latest_user_input = user_messages[-1]

        state = {
            "user_prompt": latest_user_input,
            "user_context": None,
            "analysis": None
        }

        result = agent_app.invoke(state)

        agent_output = result.get("analysis")

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

# ============================================================
# 8. Root endpoint
# ============================================================
@app.get("/")
def root():
    return {
        "message": "Work-Life Balance Agent API",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/work-life-balance/analyze"
        }
    }
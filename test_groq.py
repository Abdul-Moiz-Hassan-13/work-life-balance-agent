from agent_groq import agent_app

state = {
    "user_prompt": "I sleep at 3am and work 12 hours daily with no breaks. Analyze this.",
    "user_context": None,
    "analysis": None
}

result = agent_app.invoke(state)
print(result["analysis"])

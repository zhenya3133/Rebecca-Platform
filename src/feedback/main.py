def run_agent(context, input_data):
    episodic = context["memory"].episodic
    semantic = context["memory"].semantic
    episodic.store_event("user feedback")
    semantic.store_concept("feedback", input_data)
    return {"result": "feedback saved", "context": context}

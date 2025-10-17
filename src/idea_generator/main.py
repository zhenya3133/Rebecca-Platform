def run_agent(context, input_data):
    semantic = context["memory"].semantic
    episodic = context["memory"].episodic
    semantic.store_concept("new_idea", "apply AI to analytics")
    episodic.store_event(f"generated idea: {input_data}")
    return {"result": "idea generated", "context": context}

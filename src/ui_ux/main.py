def run_agent(context, input_data):
    semantic = context["memory"].semantic
    episodic = context["memory"].episodic
    semantic.store_concept("ui element", "button")
    episodic.store_event("ui interaction")
    return {"result": "ui_ux updated", "context": context}

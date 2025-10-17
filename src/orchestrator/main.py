def run_agent(context, input_data):
    episodic = context["memory"].episodic
    core = context["memory"].core
    episodic.store_event("workflow run")
    core.store_fact("orchestrator", True)
    return {"result": "orchestrator complete", "context": context}

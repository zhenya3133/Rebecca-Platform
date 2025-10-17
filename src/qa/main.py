def run_agent(context, input_data):
    episodic = context["memory"].episodic
    procedural = context["memory"].procedural
    episodic.store_event("qa check triggered")
    procedural.store_workflow("test_case", ["open app", "validate output"])
    return {"result": "qa review", "context": context}

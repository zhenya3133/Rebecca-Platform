def run_agent(context, input_data):
    episodic = context["memory"].episodic
    security_mem = context["memory"].security
    episodic.store_event("logger event")
    security_mem.store_audit("logging audit")
    return {"result": "logger complete", "context": context}

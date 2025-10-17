def run_agent(context, input_data):
    procedural = context["memory"].procedural
    episodic = context["memory"].episodic
    procedural.store_workflow("schedule", ["plan", "allocate", "execute"])
    episodic.store_event("scheduler: new round")
    return {"result": "scheduler run", "context": context}

def run_agent(context, input_data):
    core = context["memory"].core
    procedural = context["memory"].procedural
    core.store_fact("memory access", True)
    procedural.store_workflow("memory_manager", ["init", "manage", "terminate"])
    return {"result": "memory_manager active", "context": context}

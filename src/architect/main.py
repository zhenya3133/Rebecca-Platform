def run_agent(context, input_data):
    core = context["memory"].core
    semantic = context["memory"].semantic
    core.store_fact("architecture", "initialized")
    semantic.store_concept("solution pattern", "microservices")
    return {"result": "architect complete", "context": context}

def run_agent(context, input_data):
    memory = context.get("memory")
    if memory:
        memory.core.store_fact("start", "agent launched")
    return {"result": "stub", "context": context}

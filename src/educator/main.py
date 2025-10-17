def run_agent(context, input_data):
    core = context["memory"].core
    semantic = context["memory"].semantic
    core.store_fact("lesson", input_data)
    semantic.store_concept("education topic", "machine learning")
    return {"result": "educator complete", "context": context}

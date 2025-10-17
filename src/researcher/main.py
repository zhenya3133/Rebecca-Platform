def run_agent(context, input_data):
    core = context["memory"].core
    semantic = context["memory"].semantic
    core.store_fact("research", input_data)
    semantic.store_concept("research_topic", "AI research")
    return {"result": "research complete", "context": context}

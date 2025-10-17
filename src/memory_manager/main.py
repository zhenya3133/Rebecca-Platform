from .memory_manager import MemoryManager


def run_agent(context, input_data):
    memory = context.get("memory")
    if memory is None:
        memory = MemoryManager()
        context["memory"] = memory
    memory.core.store_fact("start", "agent launched")
    return {"result": "stub", "context": context}

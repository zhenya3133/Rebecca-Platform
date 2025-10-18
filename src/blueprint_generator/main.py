from logger import log_event


def run_agent(context, input_data):
    try:
        log_event(f"{__name__}: started with data {input_data}")
        procedural = context["memory"].procedural
        core = context["memory"].core
        blueprint = {
            "modules": ["ingest", "memory", "analytics"],
            "pipelines": ["collect", "enrich", "deploy"],
        }
        procedural.store_workflow("blueprint_generator", blueprint["pipelines"])
        core.store_fact("blueprint", blueprint)
        log_event(f"{__name__}: completed successfully")
        return {"result": blueprint, "context": context}
    except Exception as exc:
        log_event(f"{__name__}: error - {exc}")
        return {"result": None, "error": str(exc), "context": context}

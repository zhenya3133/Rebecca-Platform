def run_agent(context, input_data):
    procedural = context["memory"].procedural
    vault = context["memory"].vault
    procedural.store_workflow("deploy", ["build", "test", "deploy"])
    vault.store_secret("api_key", "example_api_key")
    return {"result": "codegen complete", "context": context}

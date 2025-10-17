def run_agent(context, input_data):
    vault = context["memory"].vault
    procedural = context["memory"].procedural
    vault.store_secret("integration_token", "example_token")
    procedural.store_workflow("sync", ["connect API", "transfer data"])
    return {"result": "integration complete", "context": context}

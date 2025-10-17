def run_agent(context, input_data):
    security_mem = context["memory"].security
    vault = context["memory"].vault
    security_mem.store_audit("checked user access")
    vault.store_secret("root_password", "changeme")
    return {"result": "security audit", "context": context}

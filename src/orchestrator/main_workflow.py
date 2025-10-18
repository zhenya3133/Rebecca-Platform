# orchestrator pipeline
from architect.main import run_agent as run_architect
from researcher.main import run_agent as run_researcher
from knowledge_curator.main import run_agent as run_knowledge_curator
from blueprint_generator.main import run_agent as run_blueprint_generator
from codegen.main import run_agent as run_codegen
from qa_guardian.main import run_agent as run_qa_guardian
from sec_ops.main import run_agent as run_sec_ops
from deployment_ops.main import run_agent as run_deployment_ops
from ops_commander.main import run_agent as run_ops_commander
from feedback.main import run_agent as run_feedback
from integration.main import run_agent as run_integration
from platform_logger.platform_logger_main import run_agent as run_platform_logger
from memory_manager import memory_manager
from memory_manager.main import run_agent as run_memory_manager
from scheduler.main import run_agent as run_scheduler
from security.main import run_agent as run_security
from ui_ux.main import run_agent as run_ui_ux

def main_workflow(task_data):
    context = {}
    memory = memory_manager.MemoryManager()
    context["memory"] = memory

    result = run_architect(context, task_data)
    result = run_researcher(result["context"], result["result"])
    result = run_knowledge_curator(result["context"], result["result"])
    result = run_blueprint_generator(result["context"], result["result"])
    result = run_codegen(result["context"], result["result"])
    result = run_qa_guardian(result["context"], result["result"])
    result = run_sec_ops(result["context"], result["result"])
    result = run_deployment_ops(result["context"], result["result"])
    result = run_ops_commander(result["context"], result["result"])
    result = run_feedback(result["context"], result["result"])
    result = run_integration(result["context"], result["result"])
    result = run_platform_logger(result["context"], result["result"])
    result = run_memory_manager(result["context"], result["result"])
    result = run_scheduler(result["context"], result["result"])
    result = run_security(result["context"], result["result"])
    result = run_ui_ux(result["context"], result["result"])
    return result

def test_main_workflow():
    task_data = {"task": "Hello world example"}
    result = main_workflow(task_data)
    print("Workflow result:", result)

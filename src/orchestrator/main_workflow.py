# orchestrator pipeline
from architect.main import run_agent as run_architect
from codegen.main import run_agent as run_codegen
from educator.main import run_agent as run_educator
from feedback.main import run_agent as run_feedback
from idea_generator.main import run_agent as run_idea_generator
from integration.main import run_agent as run_integration
from logger.main import run_agent as run_logger
from memory_manager.main import run_agent as run_memory_manager
from qa.main import run_agent as run_qa
from researcher.main import run_agent as run_researcher
from scheduler.main import run_agent as run_scheduler
from security.main import run_agent as run_security
from ui_ux.main import run_agent as run_ui_ux

def main_workflow(task_data):
    context = {}
    result = run_architect(context, task_data)
    result = run_codegen(result["context"], result["result"])
    result = run_educator(result["context"], result["result"])
    result = run_feedback(result["context"], result["result"])
    result = run_idea_generator(result["context"], result["result"])
    result = run_integration(result["context"], result["result"])
    result = run_logger(result["context"], result["result"])
    result = run_memory_manager(result["context"], result["result"])
    result = run_qa(result["context"], result["result"])
    result = run_researcher(result["context"], result["result"])
    result = run_scheduler(result["context"], result["result"])
    result = run_security(result["context"], result["result"])
    result = run_ui_ux(result["context"], result["result"])
    return result

def test_main_workflow():
    task_data = {"task": "Hello world example"}
    result = main_workflow(task_data)
    print("Workflow result:", result)

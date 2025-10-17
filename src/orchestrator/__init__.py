"""Meta-Orchestrator scaffold package for Rebecca-Platform."""

from .main_loop import MetaOrchestratorLoop
from .task_manager import TaskManager
from .context_handler import ContextHandler
from .messaging import MessagingClient

__all__ = [
    "MetaOrchestratorLoop",
    "TaskManager",
    "ContextHandler",
    "MessagingClient",
]

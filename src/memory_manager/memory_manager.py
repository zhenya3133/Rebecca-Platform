from .core_memory import CoreMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .procedural_memory import ProceduralMemory
from .vault_memory import VaultMemory
from .security_memory import SecurityMemory
from .adaptive_blueprint import AdaptiveBlueprintTracker

class MemoryManager:
    def __init__(self):
        self.core = CoreMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()
        self.vault = VaultMemory()
        self.security = SecurityMemory()
        self.blueprint_tracker = AdaptiveBlueprintTracker(self.semantic)

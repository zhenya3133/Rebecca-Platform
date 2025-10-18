"""Adaptive blueprint tracker for maintaining architecture lineage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AdaptiveBlueprintTracker:
    semantic_layer: Any
    history: List[Dict[str, Any]] = field(default_factory=list)

    def record_blueprint(self, blueprint: Dict[str, Any]) -> None:
        self.history.append(blueprint)
        self.semantic_layer.store_concept("blueprint_snapshot", blueprint)

    def latest(self) -> Dict[str, Any] | None:
        return self.history[-1] if self.history else None

    def link_resource(self, identifier: str, resource: Dict[str, Any]) -> None:
        envelope = {"identifier": identifier, "resource": resource}
        self.semantic_layer.store_concept(f"resource::{identifier}", envelope)

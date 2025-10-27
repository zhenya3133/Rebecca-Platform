"""Ingest utilities to populate memory, storage, and indexes."""

from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

from event_graph.event_graph import InMemoryEventGraph
from .ingestion_models import IngestRecord
from memory_manager.memory_manager import MemoryManager
from schema.nodes import Event, Fact
from storage.graph_view import InMemoryGraphView
from storage.object_store import InMemoryObjectStore
from storage.pg_dao import InMemoryDAO
from retrieval.indexes import InMemoryBM25Index, InMemoryVectorIndex, InMemoryGraphIndex


class IngestPipeline:
    def __init__(
        self,
        memory: MemoryManager,
        dao: InMemoryDAO,
        bm25: InMemoryBM25Index,
        vec: InMemoryVectorIndex,
        graph_idx: InMemoryGraphIndex,
        graph_view: InMemoryGraphView,
        object_store: InMemoryObjectStore,
    ) -> None:
        self.memory = memory
        self.dao = dao
        self.bm25 = bm25
        self.vec = vec
        self.graph_idx = graph_idx
        self.graph_view = graph_view
        self.object_store = object_store

    def ingest_pdf(self, pdf_path: str) -> Event:
        payload = Path(pdf_path).read_bytes() if Path(pdf_path).exists() else b""
        object_key = f"pdfs/{Path(pdf_path).name}"
        self.object_store.put(object_key, payload)

        event = Event(
            id=f"pdf::{Path(pdf_path).stem}",
            ntype="Event",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            owner="system",
            privacy="team",
            confidence=0.9,
            attrs={"text": f"PDF ingest {pdf_path}"},
            t_start=datetime.utcnow(),
            actors=["pipeline"],
            channel="pdf",
            raw_ref=object_key,
        )
        self.dao.upsert_node(event.model_dump())
        self.bm25.upsert(event.id, event.attrs["text"])
        self.vec.upsert(event.id, [0.1, 0.2, 0.3])
        self.graph_view.upsert_event(event)
        self.graph_idx.set_neighbors(event.id, [])

        self.memory.episodic.store_event({"id": event.id, "summary": event.attrs["text"]})
        self.memory.blueprint_tracker.link_resource(event.id, {"type": "pdf", "path": pdf_path})
        return event

    def ingest_facts(self, facts: Iterable[Fact]) -> None:
        for fact in facts:
            self.dao.upsert_node(fact.model_dump())
            self.bm25.upsert(fact.id, fact.object)
            self.vec.upsert(fact.id, [0.5, 0.4, 0.3])


class IngestionRecord(IngestRecord):
    pass

from collections import defaultdict
from typing import Dict, Iterable, Tuple

from .scorers import fusion_score


class HybridRetriever:
    def __init__(self, dao, graph_view, bm25_idx, vec_idx):
        self.dao = dao
        self.graph = graph_view
        self.bm25 = bm25_idx
        self.vec = vec_idx

    def _as_dict(self, items: Iterable[Tuple[str, float]]) -> Dict[str, float]:
        scores: Dict[str, float] = defaultdict(float)
        for idx, score in items:
            scores[idx] = max(scores[idx], score)
        return scores

    def retrieve(self, query: str, k: int = 40):
        bm = self._as_dict(self.bm25.search(query, k * 2))
        ve = self._as_dict(self.vec.search(query, k * 2))
        gr = self._as_dict(self.graph.search_related(query, k * 2))

        all_ids = set(bm) | set(ve) | set(gr)
        fused = []
        for idx in all_ids:
            score = fusion_score(bm.get(idx, 0.0), ve.get(idx, 0.0), gr.get(idx, 0.0))
            fused.append((idx, score))

        fused.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, _ in fused[:k]:
            node = self.dao.fetch_node(idx)
            if node:
                results.append(node)
        return results

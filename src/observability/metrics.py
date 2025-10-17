"""Retrieval quality metrics for observability and regression tracking."""


def coverage_at_k(retrieved, ground_truth, k=5):
    topk = set(retrieved[:k])
    gt = set(ground_truth)
    if not gt:
        return 0.0
    return len(topk & gt) / min(len(gt), k)


def contradiction_rate(contexts):
    contradictions = [c for c in contexts if "contradiction" in str(c) or "error" in str(c)]
    return len(contradictions) / max(1, len(contexts))


def token_efficiency(retrieved, token_budget):
    if token_budget <= 0:
        return 0.0
    tokens = sum(len(str(c).split()) for c in retrieved)
    return tokens / token_budget

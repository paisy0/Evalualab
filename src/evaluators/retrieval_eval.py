from __future__ import annotations

import math

from src.config import thresholds

__all__ = ["run_retrieval_eval", "precision_at_k", "recall_at_k", "ndcg_at_k"]


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if k <= 0:
        return 0.0
    top_k = retrieved[:k]
    return sum(1 for doc in top_k if doc in relevant) / k


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    top_k = retrieved[:k]
    return sum(1 for doc in top_k if doc in relevant) / len(relevant)


def ndcg_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    dcg = sum(
        1.0 / math.log2(i + 2)
        for i, doc in enumerate(retrieved[:k])
        if doc in relevant
    )
    ideal = sum(
        1.0 / math.log2(i + 2)
        for i in range(min(len(relevant), k))
    )
    return dcg / ideal if ideal > 0 else 0.0


def run_retrieval_eval(
    query: str,
    retrieved: list[str],
    relevant: list[str],
    k: int = 5,
    precision_threshold: float | None = None,
    recall_threshold: float | None = None,
) -> dict:
    p_min = precision_threshold or thresholds.precision_min
    r_min = recall_threshold or thresholds.recall_min
    relevant_set = set(relevant)

    p = precision_at_k(retrieved, relevant_set, k)
    r = recall_at_k(retrieved, relevant_set, k)
    n = ndcg_at_k(retrieved, relevant_set, k)

    return {
        "query":       query,
        "precision_k": round(p, 4),
        "recall_k":    round(r, 4),
        "ndcg_k":      round(n, 4),
        "k":           k,
        "passed":      p >= p_min and r >= r_min,
    }

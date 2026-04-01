from __future__ import annotations

from difflib import SequenceMatcher

from src.config import thresholds

__all__ = [
    "run_text_eval",
    "check_keywords",
    "check_length",
    "check_consistency",
]


def check_keywords(answer: str, expected: list[str]) -> dict:
    lower = answer.lower()
    missing = [kw for kw in expected if kw.lower() not in lower]
    return {"all_present": len(missing) == 0, "missing": missing}


def check_length(
    answer: str,
    min_words: int | None = None,
    max_words: int | None = None,
) -> dict:
    lo = thresholds.min_answer_words if min_words is None else min_words
    hi = thresholds.max_answer_words if max_words is None else max_words
    n = len(answer.split())

    return {
        "word_count": n,
        "too_short": n < lo,
        "too_long": n > hi,
        "length_ok": lo <= n <= hi,
    }


def check_consistency(answer_a: str, answer_b: str) -> dict:
    score = SequenceMatcher(None, answer_a, answer_b).ratio()
    return {
        "similarity": round(score, 4),
        "consistent": score >= thresholds.consistency_min,
    }


def run_text_eval(
    query: str,
    answer: str,
    expected_keywords: list[str] | None = None,
    min_words: int | None = None,
    max_words: int | None = None,
    reference_answer: str | None = None,
) -> dict:
    kw = check_keywords(answer, expected_keywords or [])
    ln = check_length(answer, min_words, max_words)
    consistency = (
        check_consistency(answer, reference_answer)
        if reference_answer not in (None, "")
        else None
    )
    consistency_ok = None if consistency is None else consistency["consistent"]

    return {
        "query": query,
        "keywords_ok": kw["all_present"],
        "missing_keywords": kw["missing"],
        "length_ok": ln["length_ok"],
        "word_count": ln["word_count"],
        "consistency_ok": consistency_ok,
        "consistency_score": None if consistency is None else consistency["similarity"],
        "passed": kw["all_present"] and ln["length_ok"] and (consistency_ok is not False),
    }

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
    lo = min_words or thresholds.min_answer_words
    hi = max_words or thresholds.max_answer_words
    n = len(answer.split())

    return {
        "word_count": n,
        "too_short":  n < lo,
        "too_long":   n > hi,
        "length_ok":  lo <= n <= hi,
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
) -> dict:
    kw = check_keywords(answer, expected_keywords or [])
    ln = check_length(answer, min_words, max_words)

    return {
        "query":            query,
        "keywords_ok":      kw["all_present"],
        "missing_keywords": kw["missing"],
        "length_ok":        ln["length_ok"],
        "word_count":       ln["word_count"],
        "passed":           kw["all_present"] and ln["length_ok"],
    }

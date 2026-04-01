#!/usr/bin/env python3
from __future__ import annotations

import json
import argparse
import logging
import sys

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    mapping = config.get("mapping", {})
    list_cols = config.get("list_cols", ["retrieved_docs", "relevant_docs", "expected_keywords"])
    default_query = config.get("default_query", "SELECT * FROM eval_log LIMIT 100")

from src.evaluators import run_retrieval_eval, run_sql_eval, run_text_eval
from src.exceptions import EvalLabError
from src.pipeline import run_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-5s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("eval-lab")

_DISPATCH = {
    "retrieval": lambda c: run_retrieval_eval(
        query=c["query"],
        retrieved=c.get("retrieved", []),
        relevant=c.get("relevant", []),
        k=c.get("k", 5),
    ),
    "sql": lambda c: run_sql_eval(
        query=c["query"],
        sql=c.get("sql", ""),
        expected_keywords=c.get("expected_keywords"),
    ),
    "text": lambda c: run_text_eval(
        query=c["query"],
        answer=c.get("answer", ""),
        expected_keywords=c.get("expected_keywords"),
    ),
}

def _evaluate(test_cases: list[dict], *, save: bool = True) -> list[dict]:
    results = []
    skipped = 0

    for i, case in enumerate(test_cases, 1):
        eval_type = case.get("type", "")
        handler = _DISPATCH.get(eval_type)
        if handler is None:
            log.warning(
                "[%d/%d] unknown type '%s', skipping → %s",
                i, len(test_cases), eval_type, case.get("query", "?"),
            )
            skipped += 1
            continue

        result = handler(case)
        result["eval_type"] = eval_type
        results.append(result)

    if skipped:
        log.warning("skipped %d/%d (unknown eval types)", skipped, len(test_cases))

    run_report(results, save=save)
    return results

def _load_from_db(db_type: str, query: str | None = None) -> list[dict]:
    from src.loaders import get_loader, normalize

    sql = query or default_query

    log.info("loading from %s → %s", db_type, sql[:80])

    with get_loader(db_type) as db:
        raw = db.fetch(sql)

    log.info("fetched %d rows", len(raw))
    return normalize(raw, mapping, list_columns=list_cols, preserve_unmapped=True)

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="ai-eval-lab",
        description="Run the AI evaluation pipeline.",
    )
    parser.add_argument("--db", choices=["postgres", "pg", "mysql"], required=True,
                        help="DB type.")
    parser.add_argument("--query", type=str, default=None,
                        help="Custom SQL to fetch test cases from DB.")
    parser.add_argument("--no-save", action="store_true",
                        help="Skip CSV/JSON export.")
    args = parser.parse_args()

    try:
        cases = _load_from_db(args.db, args.query)
    except EvalLabError as e:
        log.error("DB load failed: %s", e)
        return 1

    if not cases:
        log.error("0 test cases found. nothing to do.")
        return 1

    log.info("evaluating %d cases...", len(cases))
    results = _evaluate(cases, save=not args.no_save)

    passed = sum(1 for r in results if r.get("passed"))
    log.info("done → %d/%d passed", passed, len(results))
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""
Pipeline integration test — runs the full eval loop with demo data.

  1. Alttaki commented bloğun yorumunu kaldır
  2. MAPPING ve LIST_COLS'u kendi DB şemana göre düzenle
  3. test_cases satırını sil

"""

from __future__ import annotations

import logging

from src.evaluators import run_retrieval_eval, run_sql_eval, run_text_eval
from src.pipeline import run_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-5s │ %(message)s",
    datefmt="%H:%M:%S",
)

# ── DB────────────────────────────────────
# from src.loaders import get_loader, normalize
#
# MAPPING = {
#     "soru_kolonu":      "query",
#     "cevap_kolonu":     "answer",
#     "belgeler_kolonu":  "retrieved_docs",
#     "ilgili_kolonu":    "relevant_docs",
#     "sql_kolonu":       "sql",
#     "tip_kolonu":       "type",
#     "keyword_kolonu":   "expected_keywords",
# }
# LIST_COLS = ["retrieved_docs", "relevant_docs", "expected_keywords"]
#
# with get_loader("postgres") as db:
#     raw = db.fetch("SELECT * FROM eval_log LIMIT 100")
#     test_cases = normalize(raw, MAPPING, list_columns=LIST_COLS,
#                            preserve_unmapped=True)
# ───────────────────────────────────────────────────────────────


# demo data — DB gelince sil
test_cases = [
    {
        "type":      "retrieval",
        "query":     "Revenue of company A",
        "retrieved": ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"],
        "relevant":  ["doc_1", "doc_2", "doc_5", "doc_6"],
        "k":         5,
    },
    {
        "type":              "sql",
        "query":             "Monthly sales total",
        "sql":               "SELECT month, SUM(sales) FROM orders GROUP BY month",
        "expected_keywords": ["SELECT", "GROUP BY"],
    },
    {
        "type":              "sql",
        "query":             "Get all users",
        "sql":               "SELEC * FORM users",
        "expected_keywords": ["SELECT"],
    },
    {
        "type":              "text",
        "query":             "Revenue of company A in January?",
        "answer":            "Company A had revenue of 1.2M in January.",
        "expected_keywords": ["revenue", "january"],
    },
    {
        "type":              "text",
        "query":             "Cost breakdown for Q1?",
        "answer":            "The weather was nice.",
        "expected_keywords": ["cost", "q1"],
    },
]


# ── dispatch ───────────────────────────────────────────────────
_HANDLERS = {
    "retrieval": lambda c: run_retrieval_eval(
        query=c["query"], retrieved=c["retrieved"],
        relevant=c["relevant"], k=c.get("k", 5),
    ),
    "sql": lambda c: run_sql_eval(
        query=c["query"], sql=c["sql"],
        expected_keywords=c.get("expected_keywords"),
    ),
    "text": lambda c: run_text_eval(
        query=c["query"], answer=c["answer"],
        expected_keywords=c.get("expected_keywords"),
    ),
}

results = []
for case in test_cases:
    handler = _HANDLERS.get(case.get("type"))
    if handler is None:
        logging.warning("unknown type '%s' → skip", case.get("type"))
        continue
    result = handler(case)
    result["eval_type"] = case["type"]
    results.append(result)

run_report(results, save=True)

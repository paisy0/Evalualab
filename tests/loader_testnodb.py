from src.loaders.normalizer import normalize

_FAKE_ROWS = [
    {
        "user_question":   "What is revenue?",
        "system_response": "It is 100k.",
        "doc_ids":         "doc_1,doc_2,doc_3",
        "relevant_ids":    '["doc_1", "doc_2"]',
        "eval_type":       "retrieval",
        "extra_field":     "should survive if preserve=True",
    },
    {
        "user_question":   "Show monthly sales",
        "system_response": "SELECT month, SUM(s) FROM orders GROUP BY month",
        "doc_ids":         "doc_5",
        "relevant_ids":    None,
        "eval_type":       "sql",
        "extra_field":     "row 2 extra",
    },
]

_MAPPING = {
    "user_question":   "query",
    "system_response": "answer",
    "doc_ids":         "retrieved_docs",
    "relevant_ids":    "relevant_docs",
    "eval_type":       "type",
}

_LIST_COLS = ["retrieved_docs", "relevant_docs"]

rows = normalize(_FAKE_ROWS, _MAPPING, list_columns=_LIST_COLS, preserve_unmapped=True)

print("With preserve_unmapped=True:")
for i, row in enumerate(rows):
    print(f"\n  Row {i}:")
    for k, v in row.items():
        print(f"    {k:<20}: {v!r}")

r0, r1 = rows

assert r0["retrieved_docs"] == ["doc_1", "doc_2", "doc_3"], "CSV split failed"
assert r0["relevant_docs"]  == ["doc_1", "doc_2"],          "JSON parse failed"
assert r0["query"]          == "What is revenue?",           "mapping broken"
assert "extra_field" in r0,                                  "preserve_unmapped lost data"

assert r1["retrieved_docs"] == ["doc_5"],                    "single item → list failed"
assert r1["relevant_docs"]  == [],                           "None → [] failed"

rows_slim = normalize(_FAKE_ROWS, _MAPPING, list_columns=_LIST_COLS, preserve_unmapped=False)

assert "extra_field" not in rows_slim[0], "extra leaked through"
assert "extra_field" not in rows_slim[1], "extra leaked through"

print("\n[OK] all normalizer assertions passed")

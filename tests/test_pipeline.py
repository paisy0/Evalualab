from __future__ import annotations

import pytest

import main
import src.loaders
from src.exceptions import ConfigurationError


class _Loader:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return None

    def fetch(self, query: str) -> list[dict]:
        assert query == "SELECT * FROM real_eval_log"
        return self._rows


def test_load_from_db_uses_env_mapping(monkeypatch):
    monkeypatch.setenv("EVAL_SOURCE_QUERY", "SELECT * FROM real_eval_log")
    monkeypatch.setenv("EVAL_COL_QUERY", "question_col")
    monkeypatch.setenv("EVAL_COL_TYPE", "type_col")
    monkeypatch.setenv("EVAL_COL_RETRIEVED", "retrieved_col")
    monkeypatch.setenv("EVAL_COL_RELEVANT", "relevant_col")
    monkeypatch.setenv("EVAL_COL_K", "k_col")

    rows = [
        {
            "question_col": "q",
            "type_col": "retrieval",
            "retrieved_col": "doc_1,doc_2",
            "relevant_col": '["doc_1"]',
            "k_col": "3",
        }
    ]

    monkeypatch.setattr(src.loaders, "get_loader", lambda db_type: _Loader(rows))

    [case] = main._load_from_db("postgres")

    assert case["query"] == "q"
    assert case["type"] == "retrieval"
    assert case["retrieved"] == ["doc_1", "doc_2"]
    assert case["relevant"] == ["doc_1"]
    assert case["k"] == "3"


def test_evaluate_dispatches_normalized_retrieval(monkeypatch):
    monkeypatch.setattr(main, "run_report", lambda results, save=True: None)

    results = main._evaluate(
        [
            {
                "type": "retrieval",
                "query": "q",
                "retrieved": ["doc_1"],
                "relevant": ["doc_1"],
                "k": "1",
            }
        ],
        save=False,
    )

    assert len(results) == 1
    assert results[0]["passed"] is True


def test_load_from_db_raises_on_missing_required_column(monkeypatch):
    monkeypatch.setenv("EVAL_SOURCE_QUERY", "SELECT * FROM real_eval_log")
    monkeypatch.setenv("EVAL_COL_QUERY", "question_col")
    monkeypatch.setenv("EVAL_COL_TYPE", "type_col")
    monkeypatch.setenv("EVAL_COL_RETRIEVED", "retrieved_col")
    monkeypatch.setenv("EVAL_COL_RELEVANT", "relevant_col")

    rows = [
        {
            "question_col": "q",
            "type_col": "retrieval",
            "relevant_col": '["doc_1"]',
        }
    ]

    monkeypatch.setattr(src.loaders, "get_loader", lambda db_type: _Loader(rows))

    with pytest.raises(ConfigurationError, match="Missing column: retrieved_col"):
        main._load_from_db("postgres")


def test_load_from_db_raises_on_empty_retrieval_value(monkeypatch):
    monkeypatch.setenv("EVAL_SOURCE_QUERY", "SELECT * FROM real_eval_log")
    monkeypatch.setenv("EVAL_COL_QUERY", "question_col")
    monkeypatch.setenv("EVAL_COL_TYPE", "type_col")
    monkeypatch.setenv("EVAL_COL_RETRIEVED", "retrieved_col")
    monkeypatch.setenv("EVAL_COL_RELEVANT", "relevant_col")

    rows = [
        {
            "question_col": "q",
            "type_col": "retrieval",
            "retrieved_col": "",
            "relevant_col": '["doc_1"]',
        }
    ]

    monkeypatch.setattr(src.loaders, "get_loader", lambda db_type: _Loader(rows))

    with pytest.raises(ConfigurationError, match="Missing field: retrieved_col"):
        main._load_from_db("postgres")


def test_load_from_db_raises_on_missing_sql_keywords_mapping(monkeypatch):
    monkeypatch.setenv("EVAL_SOURCE_QUERY", "SELECT * FROM real_eval_log")
    monkeypatch.setenv("EVAL_COL_QUERY", "question_col")
    monkeypatch.setenv("EVAL_COL_TYPE", "type_col")
    monkeypatch.setenv("EVAL_COL_SQL", "sql_col")

    rows = [
        {
            "question_col": "q",
            "type_col": "sql",
            "sql_col": "SELECT 1",
        }
    ]

    monkeypatch.setattr(src.loaders, "get_loader", lambda db_type: _Loader(rows))

    with pytest.raises(ConfigurationError, match="Missing mapping: EVAL_COL_KEYWORDS"):
        main._load_from_db("postgres")


def test_load_from_db_raises_on_missing_text_reference_mapping(monkeypatch):
    monkeypatch.setenv("EVAL_SOURCE_QUERY", "SELECT * FROM real_eval_log")
    monkeypatch.setenv("EVAL_COL_QUERY", "question_col")
    monkeypatch.setenv("EVAL_COL_TYPE", "type_col")
    monkeypatch.setenv("EVAL_COL_ANSWER", "answer_col")
    monkeypatch.setenv("EVAL_COL_KEYWORDS", "keywords_col")

    rows = [
        {
            "question_col": "q",
            "type_col": "text",
            "answer_col": "answer",
            "keywords_col": '["answer"]',
        }
    ]

    monkeypatch.setattr(src.loaders, "get_loader", lambda db_type: _Loader(rows))

    with pytest.raises(ConfigurationError, match="Missing mapping: EVAL_COL_REFERENCE_ANSWER"):
        main._load_from_db("postgres")


def test_evaluate_raises_on_missing_sql_value(monkeypatch):
    monkeypatch.setattr(main, "run_report", lambda results, save=True: None)

    with pytest.raises(ConfigurationError, match="Missing field: sql"):
        main._evaluate(
            [
                {
                    "type": "sql",
                    "query": "q",
                }
            ],
            save=False,
        )

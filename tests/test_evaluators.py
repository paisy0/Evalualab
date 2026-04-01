from src.evaluators import run_retrieval_eval, run_sql_eval, run_text_eval


def test_retrieval_eval_accepts_zero_thresholds():
    result = run_retrieval_eval(
        query="q",
        retrieved=["doc_1"],
        relevant=["doc_1"],
        k=1,
        precision_threshold=0.0,
        recall_threshold=0.0,
    )

    assert result["passed"] is True


def test_sql_eval_matches_keywords_as_tokens():
    result = run_sql_eval(
        query="q",
        sql="SELECT * FROM orders",
        expected_keywords=["OR"],
    )

    assert result["syntax_valid"] is True
    assert result["keywords_ok"] is False
    assert result["missing_keywords"] == ["OR"]


def test_text_eval_uses_reference_answer_when_present():
    result = run_text_eval(
        query="q",
        answer="same answer",
        expected_keywords=["same"],
        min_words=0,
        reference_answer="same answer",
    )

    assert result["length_ok"] is True
    assert result["consistency_ok"] is True
    assert result["passed"] is True

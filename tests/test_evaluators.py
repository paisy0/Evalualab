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


def test_retrieval_eval_uses_ndcg_for_pass_fail():
    result = run_retrieval_eval(
        query="q",
        retrieved=["doc_x", "doc_1", "doc_2"],
        relevant=["doc_1", "doc_2"],
        k=3,
        precision_threshold=0.5,
        recall_threshold=1.0,
        ndcg_threshold=0.8,
    )

    assert result["precision_k"] == 0.6667
    assert result["recall_k"] == 1.0
    assert result["ndcg_k"] == 0.6934
    assert result["passed"] is False


def test_sql_eval_matches_keywords_as_tokens():
    result = run_sql_eval(
        query="q",
        sql="SELECT * FROM orders",
        expected_keywords=["OR"],
    )

    assert result["syntax_valid"] is True
    assert result["keywords_ok"] is False
    assert result["missing_keywords"] == ["OR"]


def test_sql_eval_requires_keywords_for_pass():
    result = run_sql_eval(
        query="q",
        sql="SELECT 1",
    )

    assert result["syntax_valid"] is True
    assert result["keywords_checked"] is False
    assert result["keywords_ok"] is False
    assert result["passed"] is False


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


def test_text_eval_requires_keywords_and_reference_for_pass():
    result = run_text_eval(
        query="q",
        answer="this answer is long enough to pass length",
        min_words=0,
    )

    assert result["keywords_checked"] is False
    assert result["consistency_checked"] is False
    assert result["passed"] is False


def test_text_eval_matches_keywords_as_tokens():
    result = run_text_eval(
        query="q",
        answer="orders summary",
        expected_keywords=["or"],
        min_words=0,
        reference_answer="orders summary",
    )

    assert result["keywords_ok"] is False
    assert result["missing_keywords"] == ["or"]
    assert result["passed"] is False

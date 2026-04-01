from src.evaluators import run_retrieval_eval, run_sql_eval, run_text_eval


def _section(title: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print("=" * 50)


def _dump(result: dict) -> None:
    for k, v in result.items():
        print(f"  {k:<20} : {v}")


_section("RETRIEVAL EVAL")
_dump(run_retrieval_eval(
    query="What is the revenue of company A?",
    retrieved=["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"],
    relevant=["doc_1", "doc_2", "doc_5", "doc_6"],
    k=5,
))

_section("SQL EVAL — valid")
_dump(run_sql_eval(
    query="Monthly sales total",
    sql="SELECT month, SUM(sales) FROM orders GROUP BY month",
    expected_keywords=["SELECT", "GROUP BY"],
))

_section("SQL EVAL — broken")
_dump(run_sql_eval(
    query="Get all users",
    sql="SELEC * FORM users",
    expected_keywords=["SELECT"],
))

_section("TEXT EVAL")
_dump(run_text_eval(
    query="What is the revenue of company A in January?",
    answer="Company A had a total revenue of 1.2 million in January. Costs were 800k.",
    expected_keywords=["revenue", "january"],
))

print("\n[OK] all evaluators operational")

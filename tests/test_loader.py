import pytest

from src.exceptions import UnknownLoader
from src.loaders.loader_factory import get_loader
from src.loaders.mysql_loader import MySQLLoader
from src.loaders.normalizer import normalize
from src.loaders.postgres_loader import PostgresLoader


def test_get_loader_returns_registered_loader():
    assert isinstance(get_loader("postgres"), PostgresLoader)
    assert isinstance(get_loader("pg"), PostgresLoader)
    assert isinstance(get_loader("mysql"), MySQLLoader)


def test_get_loader_rejects_unknown_type():
    with pytest.raises(UnknownLoader):
        get_loader("sqlite")


def test_normalize_preserves_unmapped_columns():
    rows = [
        {
            "question_col": "q",
            "retrieved_col": "doc_1,doc_2",
            "relevant_col": '["doc_1"]',
            "type_col": "retrieval",
            "extra_col": "x",
        }
    ]
    mapping = {
        "question_col": "query",
        "retrieved_col": "retrieved",
        "relevant_col": "relevant",
        "type_col": "type",
    }

    [row] = normalize(
        rows,
        mapping,
        list_columns=["retrieved", "relevant"],
        preserve_unmapped=True,
    )

    assert row["query"] == "q"
    assert row["retrieved"] == ["doc_1", "doc_2"]
    assert row["relevant"] == ["doc_1"]
    assert row["extra_col"] == "x"

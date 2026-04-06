import json

import pytest

from src.exceptions import ConfigurationError
from src.loaders.file_loader import load_csv_cases, load_json_cases
from src.loaders.normalizer import normalize
from src.path_utils import display_path


def test_normalize_drops_unmapped_columns_when_requested():
    rows = [
        {
            "query_col": "q",
            "docs_col": "doc_1",
            "extra_col": "x",
        }
    ]
    mapping = {
        "query_col": "query",
        "docs_col": "retrieved",
    }

    [row] = normalize(
        rows,
        mapping,
        list_columns=["retrieved"],
        preserve_unmapped=False,
    )

    assert row == {
        "query": "q",
        "retrieved": ["doc_1"],
    }


def test_normalize_handles_none_list_values():
    rows = [
        {
            "query_col": "q",
            "docs_col": None,
        }
    ]
    mapping = {
        "query_col": "query",
        "docs_col": "retrieved",
    }

    [row] = normalize(
        rows,
        mapping,
        list_columns=["retrieved"],
    )

    assert row["retrieved"] == []


def test_load_json_cases_normalizes_list_columns(tmp_path):
    path = tmp_path / "cases.json"
    path.write_text(
        json.dumps(
            [
                {
                    "type": "retrieval",
                    "query": "q",
                    "retrieved": "doc_1,doc_2",
                    "relevant": ["doc_1"],
                }
            ]
        ),
        encoding="utf-8",
    )

    [case] = load_json_cases(str(path))

    assert case["retrieved"] == ["doc_1", "doc_2"]
    assert case["relevant"] == ["doc_1"]


def test_load_csv_cases_normalizes_list_columns(tmp_path):
    path = tmp_path / "cases.csv"
    path.write_text(
        "type,query,expected_keywords\nsql,q,\"SELECT,FROM\"\n",
        encoding="utf-8",
    )

    [case] = load_csv_cases(str(path))

    assert case["expected_keywords"] == ["SELECT", "FROM"]


def test_load_json_cases_rejects_invalid_shape(tmp_path):
    path = tmp_path / "cases.json"
    path.write_text(json.dumps({"bad": []}), encoding="utf-8")

    with pytest.raises(ConfigurationError, match="JSON input must be a list of rows."):
        load_json_cases(str(path))


def test_display_path_hides_absolute_parent_directories():
    shown = display_path(r"C:\Users\secret\Desktop\private\cases.json")

    assert shown == "cases.json"

from src.loaders.normalizer import normalize


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

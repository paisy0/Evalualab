from __future__ import annotations

import json
import logging

__all__ = ["normalize"]
log = logging.getLogger(__name__)


def _to_list(value) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    if not isinstance(value, str):
        return [value]

    stripped = value.strip()
    if not stripped:
        return []

    if stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass

    return [item.strip() for item in stripped.split(",") if item.strip()]


def normalize(
    rows: list[dict],
    mapping: dict[str, str],
    *,
    list_columns: list[str] | None = None,
    preserve_unmapped: bool = False,
) -> list[dict]:
    list_cols = set(list_columns or [])
    mapped_keys = set(mapping.keys())
    result = []

    for row in rows:
        new = {}
        for src_col, dst_col in mapping.items():
            val = row.get(src_col)
            new[dst_col] = _to_list(val) if dst_col in list_cols else val
        if preserve_unmapped:
            for col, val in row.items():
                if col not in mapped_keys:
                    new[col] = val
        result.append(new)

    if not result:
        log.warning("normalizer got 0 rows — nothing to transform")

    return result

from __future__ import annotations

import sqlglot
from sqlglot import exp

__all__ = ["run_sql_eval", "check_sql_syntax", "check_sql_keywords"]

_SQL_STATEMENT_TYPES = (
    exp.Select, exp.Insert, exp.Update, exp.Delete,
    exp.Create, exp.Drop, exp.Alter, exp.Merge,
    exp.Use, exp.Set, exp.Show, exp.Describe, exp.Command,
    exp.Transaction, exp.Commit, exp.Rollback, exp.Grant,
)


def check_sql_syntax(sql: str) -> dict:
    if not sql or not sql.strip():
        return {"valid": False, "error": "Empty SQL"}

    try:
        parsed = sqlglot.parse(sql.strip())
    except sqlglot.errors.ParseError as e:
        return {"valid": False, "error": str(e)}
    except Exception as e:
        return {"valid": False, "error": f"Unexpected: {e}"}

    if not parsed or parsed[0] is None:
        return {"valid": False, "error": "Parser returned nothing"}

    stmt = parsed[0]
    if not isinstance(stmt, _SQL_STATEMENT_TYPES):
        return {
            "valid": False,
            "error": f"Not a SQL statement (got {type(stmt).__name__})",
        }

    return {"valid": True, "error": None}


def check_sql_keywords(sql: str, expected: list[str]) -> dict:
    upper = sql.upper()
    missing = [kw for kw in expected if kw.upper() not in upper]
    return {
        "all_present": len(missing) == 0,
        "missing": missing,
    }


def run_sql_eval(
    query: str,
    sql: str,
    expected_keywords: list[str] | None = None,
) -> dict:
    syntax = check_sql_syntax(sql)
    keywords = check_sql_keywords(sql, expected_keywords or [])

    return {
        "query":            query,
        "sql":              sql,
        "syntax_valid":     syntax["valid"],
        "syntax_error":     syntax["error"],
        "keywords_ok":      keywords["all_present"],
        "missing_keywords": keywords["missing"],
        "passed":           syntax["valid"] and keywords["all_present"],
    }

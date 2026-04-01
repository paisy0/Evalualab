# AI Eval Lab

Lightweight evaluation pipeline for AI system outputs stored in a database.

This repository does not generate answers, SQL, or retrieval results. It reads rows that already exist in a database, evaluates them, and produces a report.

## Current Scope

Implemented now:

- Retrieval evaluator
- SQL evaluator
- Text evaluator
- Postgres and MySQL loaders
- Result reporter

Supported metrics:

| Evaluator | Metrics |
| :--- | :--- |
| **Retrieval** | Precision@K, Recall@K, NDCG@K |
| **SQL** | Syntax validity, keyword presence |
| **Text** | Keyword coverage, answer length, consistency |

## What This Repo Does

The pipeline:

1. Connects to Postgres or MySQL.
2. Runs a source query.
3. Maps your DB columns into the evaluator schema.
4. Dispatches each row to the correct evaluator based on `type`.
5. Prints a dashboard.
6. Optionally writes CSV and JSON reports under [reports](/C:/Users/ordox/Desktop/ai-eval-lab/reports).

The pipeline evaluates existing outputs.

Examples of evaluated system outputs:

- Retrieval output: retrieved document IDs
- SQL output: generated SQL query
- Text output: generated answer text

## Project Structure

- [main.py](/C:/Users/ordox/Desktop/ai-eval-lab/main.py): entry point and evaluator dispatch
- [src/config.py](/C:/Users/ordox/Desktop/ai-eval-lab/src/config.py): env-based config and thresholds
- [src/loaders](/C:/Users/ordox/Desktop/ai-eval-lab/src/loaders): DB loaders and row normalization
- [src/evaluators](/C:/Users/ordox/Desktop/ai-eval-lab/src/evaluators): retrieval, SQL, and text evaluators
- [src/pipeline/reporter.py](/C:/Users/ordox/Desktop/ai-eval-lab/src/pipeline/reporter.py): dashboard and file exports
- [tests](/C:/Users/ordox/Desktop/ai-eval-lab/tests): unit tests

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Optional sanity check:

```bash
python setup_check.py
```

## Environment Variables

Copy [.env.example](/C:/Users/ordox/Desktop/ai-eval-lab/.env.example) and fill it:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
EVAL_SOURCE_QUERY=
EVAL_COL_QUERY=
EVAL_COL_ANSWER=
EVAL_COL_SQL=
EVAL_COL_RETRIEVED=
EVAL_COL_RELEVANT=
EVAL_COL_TYPE=
EVAL_COL_KEYWORDS=
EVAL_COL_REFERENCE_ANSWER=
EVAL_COL_K=
```

## DB Mapping

`EVAL_COL_*` values are column names, not real data.

Correct:

```env
EVAL_COL_QUERY=user_question
EVAL_COL_ANSWER=system_response
EVAL_COL_SQL=generated_sql
```

Wrong:

```env
EVAL_COL_QUERY=What is revenue?
EVAL_COL_SQL=SELECT * FROM orders
```

Meaning of each field:

- `EVAL_SOURCE_QUERY`: SQL query used to fetch rows from the database
- `EVAL_COL_QUERY`: column that stores the user question
- `EVAL_COL_ANSWER`: column that stores the generated text answer
- `EVAL_COL_SQL`: column that stores the generated SQL
- `EVAL_COL_RETRIEVED`: column that stores retrieved document IDs
- `EVAL_COL_RELEVANT`: column that stores relevant document IDs
- `EVAL_COL_TYPE`: column that stores the evaluation type
- `EVAL_COL_KEYWORDS`: column that stores expected keywords
- `EVAL_COL_REFERENCE_ANSWER`: column that stores the reference answer
- `EVAL_COL_K`: column that stores the `k` value

Expected values inside the type column:

- `retrieval`
- `sql`
- `text`

## Row Contract

Every row must include:

- `query`
- `type`

For `retrieval` rows:

- retrieved docs
- relevant docs
- optional `k`

For `sql` rows:

- generated SQL
- expected keywords

For `text` rows:

- generated answer
- expected keywords
- reference answer

If required mappings or required values are missing, the pipeline fails fast with an error instead of silently producing weak results.

## Accepted List Formats

These fields can be stored either as JSON arrays or comma-separated strings:

- retrieved docs
- relevant docs
- expected keywords

Examples:

```text
["doc_1", "doc_2"]
```

```text
doc_1,doc_2
```

## Example Mapping

If your table contains these columns:

- `user_question`
- `system_response`
- `generated_sql`
- `source_doc_ids`
- `relevant_doc_ids`
- `eval_type`
- `keywords`
- `gold_answer`
- `top_k`

then your `.env` can look like this:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_password

EVAL_SOURCE_QUERY=SELECT * FROM eval_log LIMIT 100
EVAL_COL_QUERY=user_question
EVAL_COL_ANSWER=system_response
EVAL_COL_SQL=generated_sql
EVAL_COL_RETRIEVED=source_doc_ids
EVAL_COL_RELEVANT=relevant_doc_ids
EVAL_COL_TYPE=eval_type
EVAL_COL_KEYWORDS=keywords
EVAL_COL_REFERENCE_ANSWER=gold_answer
EVAL_COL_K=top_k
```

## How Evaluation Works

### Retrieval

Input:

- query
- retrieved docs
- relevant docs
- optional `k`

Output fields include:

- `precision_k`
- `recall_k`
- `ndcg_k`
- `passed`

### SQL

Input:

- query
- SQL
- expected keywords

Output fields include:

- `syntax_valid`
- `syntax_error`
- `keywords_checked`
- `keywords_ok`
- `missing_keywords`
- `passed`

Note:

- SQL evaluation checks syntax and required keyword presence.
- It does not execute the SQL and does not verify semantic correctness of query results.

### Text

Input:

- query
- answer
- expected keywords
- reference answer

Output fields include:

- `keywords_checked`
- `keywords_ok`
- `missing_keywords`
- `length_ok`
- `word_count`
- `consistency_checked`
- `consistency_ok`
- `consistency_score`
- `passed`

## Run

```bash
python main.py --db postgres
python main.py --db pg
python main.py --db mysql
python main.py --db postgres --query "SELECT * FROM eval_log LIMIT 100"
python main.py --db postgres --no-save
```

## Reports

The reporter prints a small dashboard to stdout and, unless `--no-save` is used, writes:

- `reports/eval_results_<timestamp>.csv`
- `reports/eval_results_<timestamp>.json`

## Testing

Run all tests:

```bash
python -m pytest tests -q
```

Current test status in this workspace: `19 passed`

## Limitations

This repo is intentionally narrow at this stage.

- It evaluates outputs; it does not generate them.
- SQL evaluation is syntax and keyword based, not result-set based.
- Text consistency depends on a reference answer column.
- Retrieval quality depends on the correctness of retrieved and relevant doc IDs stored in the database.

## Roadmap

### Done

- [x] Retrieval, SQL, text evaluators + DB loader + reporter

### Next

- [ ] Synthetic test data generation (RAGAS TestsetGenerator)
- [ ] NDCG & MRR deep dive, embedding-based similarity
- [ ] LLM-as-Judge (hallucination detection, quality scoring)
- [ ] Consistency & adversarial eval
- [ ] Observability (Langfuse), regression eval, full pipeline
- [ ] CI/CD integration (Promptfoo), A/B testing, DeepEval

## Summary

This project is currently an evaluator pipeline MVP.

It is a good base for:

- scoring retrieval outputs
- checking generated SQL shape and required structure
- scoring generated text answers
- building a larger evaluation platform on top of DB-backed data

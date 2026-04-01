## AI Eval Lab

| Evaluator | Metrics |
| :--- | :--- |
| **Retrieval** | Precision@K · Recall@K · NDCG@K |
| **SQL** | Syntax validity · keyword presence |
| **Text** | Keyword coverage · answer length · consistency |

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` with:

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

### DB Mapping

`EVAL_COL_*` fields are not filled automatically after DB connection.

These fields are used to map your database schema to the pipeline.

Write the database column name on the right side, not the actual data.

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

- `EVAL_SOURCE_QUERY`: SQL query used to fetch rows from the database.
- `EVAL_COL_QUERY`: Column name that stores the user question.
- `EVAL_COL_ANSWER`: Column name that stores the text answer.
- `EVAL_COL_SQL`: Column name that stores the generated SQL.
- `EVAL_COL_RETRIEVED`: Column name that stores retrieved document IDs.
- `EVAL_COL_RELEVANT`: Column name that stores relevant document IDs.
- `EVAL_COL_TYPE`: Column name that stores the evaluation type.
- `EVAL_COL_KEYWORDS`: Column name that stores expected keywords.
- `EVAL_COL_REFERENCE_ANSWER`: Column name that stores the reference answer.
- `EVAL_COL_K`: Column name that stores the `k` value.

Expected values inside the type column:

- `retrieval`
- `sql`
- `text`

Example:

If your table has these columns:

- `user_question`
- `system_response`
- `generated_sql`
- `source_doc_ids`
- `relevant_doc_ids`
- `eval_type`
- `keywords`

Then your `.env` should look like this:

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
EVAL_COL_REFERENCE_ANSWER=
EVAL_COL_K=
```

Required fields:

- Always required: `EVAL_SOURCE_QUERY`, `EVAL_COL_QUERY`, `EVAL_COL_TYPE`
- For `retrieval` rows: `EVAL_COL_RETRIEVED`, `EVAL_COL_RELEVANT`
- For `sql` rows: `EVAL_COL_SQL`
- For `text` rows: `EVAL_COL_ANSWER`

### Run

```bash
python main.py --db postgres
python main.py --db pg
python main.py --db mysql
python main.py --db postgres --query "SELECT * FROM eval_log LIMIT 100"
python main.py --db postgres --no-save
```

`query` and `type` are required for every row.

For `retrieval` rows:
- `retrieved` and `relevant` mappings are required.

For `sql` rows:
- `sql` mapping is required.

For `text` rows:
- `answer` mapping is required.

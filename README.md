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

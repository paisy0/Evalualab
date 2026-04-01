# AI Eval Lab

Database icinde tutulan AI system outputs icin hafif bir evaluation pipeline.

Bu repository answer, SQL veya retrieval result uretmez. Database icinde zaten var olan satirlari okur, evaluate eder ve report uretir.

## Mevcut Kapsam

Su an olanlar:

- Retrieval evaluator
- SQL evaluator
- Text evaluator
- Postgres, MySQL ve SQLite loader'lari
- JSON/CSV file input
- Result reporter

Bu asamada baktigi metrics:

| Evaluator | Metrics |
| :--- | :--- |
| **Retrieval** | Precision@K, Recall@K, NDCG@K |
| **SQL** | Syntax validity, keyword presence |
| **Text** | Keyword coverage, answer length, consistency |

## Roadmap

### Tamamlananlar

- [x] Retrieval, SQL, text evaluators + DB loader + reporter

### Sonraki Adimlar

- [ ] Synthetic test data generation (RAGAS TestsetGenerator)
- [ ] NDCG & MRR deep dive, embedding-based similarity
- [ ] LLM-as-Judge (hallucination detection, quality scoring)
- [ ] Consistency & adversarial eval
- [ ] Observability (Langfuse), regression eval, full pipeline
- [ ] CI/CD integration (Promptfoo), A/B testing, DeepEval

## Su An Nasil Calisiyor

Pipeline su akisla calisir:

1. Postgres, MySQL veya SQLite'a baglanir ya da JSON/CSV file okur.
2. Source query calistirir ya da evaluator row'larini file icinden alir.
3. DB input kullaniliyorsa DB column'larini evaluator schema'ya map eder.
4. Her row'u `type` alanina gore dogru evaluator'a yollar.
5. Dashboard cikartir.
6. Istenirse `reports/` altina CSV ve JSON report yazar.

Pipeline mevcut output'lari evaluate eder.

Evaluate edilen system outputs ornekleri:

- Retrieval output: retrieved document IDs
- SQL output: generated SQL query
- Text output: generated answer text

Bu row'lari hem database uzerinden hem de dogrudan JSON/CSV file uzerinden verebilirsin.

## Proje Yapisi

- [`main.py`](main.py): entry point ve evaluator dispatch
- [`src/config.py`](src/config.py): env-based config ve thresholds
- [`src/loaders`](src/loaders): DB loader'lari, file loader'lari ve row normalization
- [`src/evaluators`](src/evaluators): retrieval, SQL ve text evaluator'lari
- [`src/pipeline/reporter.py`](src/pipeline/reporter.py): dashboard ve file export
- [`tests`](tests): unit test'ler

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
```

Istege bagli sanity check:

```bash
python setup_check.py
```

## Environment Variables

[`.env.example`](.env.example) dosyasini kopyalayip doldur:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_SQLITE_PATH=
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

`EVAL_COL_*` alanlari gercek data degil, column name icindir.

Dogru kullanim:

```env
EVAL_COL_QUERY=user_question
EVAL_COL_ANSWER=system_response
EVAL_COL_SQL=generated_sql
```

Yanlis kullanim:

```env
EVAL_COL_QUERY=What is revenue?
EVAL_COL_SQL=SELECT * FROM orders
```

Alanlarin anlami:

- `EVAL_SOURCE_QUERY`: database'den row cekmek icin kullanilan SQL query
- `DB_SQLITE_PATH`: `--db sqlite` kullanildiginda SQLite file path
- `EVAL_COL_QUERY`: user question tutan column
- `EVAL_COL_ANSWER`: generated text answer tutan column
- `EVAL_COL_SQL`: generated SQL tutan column
- `EVAL_COL_RETRIEVED`: retrieved document IDs tutan column
- `EVAL_COL_RELEVANT`: relevant document IDs tutan column
- `EVAL_COL_TYPE`: evaluation type tutan column
- `EVAL_COL_KEYWORDS`: expected keywords tutan column
- `EVAL_COL_REFERENCE_ANSWER`: reference answer tutan column
- `EVAL_COL_K`: `k` value tutan column

`type` column icinde beklenen degerler:

- `retrieval`
- `sql`
- `text`

## Row Contract

Her row'da olmasi gerekenler:

- `query`
- `type`

`retrieval` row'lari icin:

- retrieved docs
- relevant docs
- opsiyonel `k`

`sql` row'lari icin:

- generated SQL
- expected keywords

`text` row'lari icin:

- generated answer
- expected keywords
- reference answer

Gerekli mapping veya gerekli value eksikse pipeline bos veya uydurma sonuc uretmek yerine fail-fast hata verir.

## Kabul Edilen List Formatlari

Bu alanlar JSON array ya da comma-separated string olarak tutulabilir:

- retrieved docs
- relevant docs
- expected keywords

Ornek:

```text
["doc_1", "doc_2"]
```

```text
doc_1,doc_2
```

## Ornek Mapping

Eger tablonda su kolonlar varsa:

- `user_question`
- `system_response`
- `generated_sql`
- `source_doc_ids`
- `relevant_doc_ids`
- `eval_type`
- `keywords`
- `gold_answer`
- `top_k`

`.env` su sekilde olabilir:

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

SQLite ornegi:

```env
DB_SQLITE_PATH=C:\path\to\eval.sqlite
EVAL_SOURCE_QUERY=SELECT * FROM eval_log LIMIT 100
EVAL_COL_QUERY=query_text
EVAL_COL_ANSWER=answer_text
EVAL_COL_SQL=generated_sql
EVAL_COL_RETRIEVED=retrieved_docs
EVAL_COL_RELEVANT=relevant_docs
EVAL_COL_TYPE=eval_type
EVAL_COL_KEYWORDS=expected_keywords
EVAL_COL_REFERENCE_ANSWER=reference_answer
EVAL_COL_K=top_k
```

## Evaluation Nasil Calisiyor

### Retrieval

Input:

- query
- retrieved docs
- relevant docs
- opsiyonel `k`

Output field'lari:

- `precision_k`
- `recall_k`
- `ndcg_k`
- `passed`

### SQL

Input:

- query
- SQL
- expected keywords

Output field'lari:

- `syntax_valid`
- `syntax_error`
- `keywords_checked`
- `keywords_ok`
- `missing_keywords`
- `passed`

Not:

- SQL evaluation syntax ve gerekli keyword presence kontrolu yapar.
- SQL'i execute etmez ve query result'unun semantic correctness kismini dogrulamaz.

### Text

Input:

- query
- answer
- expected keywords
- reference answer

Output field'lari:

- `keywords_checked`
- `keywords_ok`
- `missing_keywords`
- `length_ok`
- `word_count`
- `consistency_checked`
- `consistency_ok`
- `consistency_score`
- `passed`

## Calistirma

```bash
python main.py --db postgres
python main.py --db pg
python main.py --db mysql
python main.py --db sqlite
python main.py --input-json cases.json
python main.py --input-csv cases.csv
python main.py --db postgres --query "SELECT * FROM eval_log LIMIT 100"
python main.py --db postgres --no-save
```

`--query` sadece `--db` ile birlikte calisir.

## File Input Format

`--input-json` veya `--input-csv` kullanildiginda row'lar dogrudan evaluator schema ile gelmelidir.

JSON ornegi:

```json
[
  {
    "type": "retrieval",
    "query": "What is the refund policy?",
    "retrieved": ["doc_1", "doc_2"],
    "relevant": ["doc_1"],
    "k": 2
  },
  {
    "type": "sql",
    "query": "Total sales in 2024",
    "sql": "SELECT SUM(amount) FROM sales WHERE year = 2024",
    "expected_keywords": ["SELECT", "SUM", "FROM", "WHERE"]
  },
  {
    "type": "text",
    "query": "Summarize the support policy",
    "answer": "Support is available on weekdays and critical issues are prioritized.",
    "expected_keywords": ["support", "weekdays", "critical"],
    "reference_answer": "Support is available during weekdays and urgent issues are prioritized."
  }
]
```

CSV ornegi:

```csv
type,query,sql,expected_keywords
sql,Total sales in 2024,"SELECT SUM(amount) FROM sales WHERE year = 2024","SELECT,SUM,FROM,WHERE"
```

JSON/CSV input icin gerekli field'lar yukaridaki row contract ile aynidir.

## Reports

Reporter stdout'a kucuk bir dashboard cikartir ve `--no-save` kullanilmazsa su ciktilari verir:

- `reports/eval_results_<timestamp>.csv`
- `reports/eval_results_<timestamp>.json`

## Test

Tum testleri calistirmak icin:

```bash
python -m pytest tests -q
```

Guncel test durumu: `26 passed`

## Kisitlar

Bu repo su asamada bilincli olarak dar kapsamli tutuldu.

- Output'lari evaluate eder; output uretmez.
- SQL evaluation syntax ve keyword bazlidir, result-set bazli degildir.
- Text consistency, reference answer column'una baglidir.
- Retrieval quality, database icindeki retrieved ve relevant doc ID'lerinin dogruluguna baglidir.

## Ozet

Bu proje su anda bir evaluator pipeline MVP'si.

Sunlar icin iyi bir temel saglar:

- retrieval output'larini skorlamak
- generated SQL'in shape ve required structure tarafini kontrol etmek
- generated text answer'lari skorlamak
- database-backed daha buyuk bir evaluation platform insa etmek

from src.loaders.loader_factory import get_loader
from src.loaders.normalizer import normalize

# --- Change these to match your real DB ---
DB_TYPE = "postgres"   # or "mysql"
TEST_QUERY = "SELECT * FROM your_table LIMIT 5"

MAPPING = {
    "your_question_column": "query",
    "your_answer_column":   "answer",
    "your_docs_column":     "retrieved_docs"
}
# ------------------------------------------

with get_loader(DB_TYPE) as loader:
    raw = loader.fetch(TEST_QUERY)
    print(f"\nRaw rows ({len(raw)} fetched):")
    for row in raw[:2]:
        print(row)

    normalized = normalize(raw, MAPPING)
    print(f"\nNormalized rows:")
    for row in normalized[:2]:
        print(row)
import importlib
import os
import sys

from dotenv import load_dotenv

from src.config import get_source_config

load_dotenv()

print(f"Python : {sys.version.split()[0]}")

installed = []
missing = []

for pkg in ["psycopg2", "mysql.connector", "sqlglot", "pytest"]:
    try:
        importlib.import_module(pkg)
        installed.append(pkg)
    except ImportError:
        missing.append(pkg)

if installed:
    print(f"Installed : {', '.join(installed)}")
if missing:
    print(f"Missing   : {', '.join(missing)}")

source = get_source_config()
mapped = sorted(source.mapping().values())
print(f"DB Host   : {'set' if os.getenv('DB_HOST') else 'NOT SET'}")
print(f"DB Name   : {'set' if os.getenv('DB_NAME') else 'NOT SET'}")
print(f"SQLite    : {'set' if os.getenv('DB_SQLITE_PATH') else 'NOT SET'}")
print(f"Source SQL: {'set' if source.query else 'NOT SET'}")
print(f"Mappings  : {', '.join(mapped) if mapped else 'NOT SET'}")

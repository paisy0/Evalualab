from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


@dataclass(frozen=True)
class DBConfig:
    host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("DB_PORT", "5432")))
    name: str = field(default_factory=lambda: os.getenv("DB_NAME", ""))
    user: str = field(default_factory=lambda: os.getenv("DB_USER", ""))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))
    timeout: int = 10

    def __repr__(self) -> str:
        return f"DBConfig({self.host}:{self.port}/{self.name}, user={self.user})"


@dataclass(frozen=True)
class EvalThresholds:
    precision_min: float = 0.5
    recall_min: float = 0.5
    min_answer_words: int = 10
    max_answer_words: int = 500
    consistency_min: float = 0.80


db = DBConfig()
thresholds = EvalThresholds()

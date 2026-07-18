from __future__ import annotations

import os
import secrets
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIRECTORY = PROJECT_DIR / "data"
VECTOR_DIRECTORY = PROJECT_DIR / ".rag_chroma"
COLLECTION_NAME = "garden_and_pesticide_manuals"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
RETRIEVAL_K = 3
MAX_HISTORY_MESSAGES = 20
MAX_NEW_TOKENS = 160
DEVELOPMENT_MODE = os.environ.get("RAG_DEVELOPMENT_MODE", "false").lower() == "true"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", secrets.token_urlsafe(32))

PDF_PATHS = (
    DATA_DIRECTORY / "env-protection-pesticides-business-manuals-applic-chapter7.pdf",
    DATA_DIRECTORY
    / "Noor-Book.com  garden pests in new zealand a popular manual for practical gardeners farmers and schools 2.pdf",
)

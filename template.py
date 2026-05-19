import os
import logging
from pathlib import Path

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s'
)

# =========================
# Project Structure
# =========================

list_of_files = [

    # -------------------------
    # Main Application
    # -------------------------
    "app.py",
    "setup.py",
    "requirements.txt",
    ".env",
    "README.md",

    # -------------------------
    # Source Package
    # -------------------------
    "src/__init__.py",

    # Config
    "src/config/__init__.py",
    "src/config/config.py",

    # PDF Processing
    "src/pdf_processing/__init__.py",
    "src/pdf_processing/pdf_loader.py",
    "src/pdf_processing/section_splitter.py",

    # Embedding
    "src/embedding/__init__.py",
    "src/embedding/embedder.py",

    # Vector Database
    "src/vectorstore/__init__.py",
    "src/vectorstore/chroma_store.py",

    # MongoDB
    "src/database/__init__.py",
    "src/database/mongo_handler.py",

    # Retrieval
    "src/retrieval/__init__.py",
    "src/retrieval/retriever.py",

    # LLM
    "src/llm/__init__.py",
    "src/llm/mcq_generator.py",

    # Evaluation
    "src/evaluation/__init__.py",
    "src/evaluation/evaluator.py",

    # Adaptive Learning
    "src/adaptive/__init__.py",
    "src/adaptive/history_manager.py",
    "src/adaptive/weak_topic_tracker.py",

    # Export
    "src/export/__init__.py",
    "src/export/kb_snapshot.py",

    # Utilities
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/helper.py",

    # Prompt Templates
    "src/prompts/__init__.py",
    "src/prompts/mcq_prompt.py",

    # Research / Notebook
    "research/trials.ipynb",

    # Data Directories
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",

    # Vector DB Storage
    "vector_store/.gitkeep",

    # Knowledge Base Snapshots
    "kb_snapshots/.gitkeep",

    # Logs
    "logs/app.log",

    # Tests
    "tests/test_pdf_loader.py",
    "tests/test_splitter.py",
    "tests/test_retrieval.py",
]

# =========================
# Create Folders and Files
# =========================

for filepath in list_of_files:

    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    # Create directories
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    # Create files
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):

        with open(filepath, "w") as f:
            pass

        logging.info(f"Created file: {filepath}")

    else:
        logging.info(f"File already exists: {filepath}")

print("\n✅ Adaptive Document Preparation System Template Created Successfully!")
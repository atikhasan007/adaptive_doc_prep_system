import fitz  # PyMuPDF
import re
from typing import Dict, List
from langchain_huggingface import HuggingFaceEmbeddings
import json
from datetime import datetime




    # ---------- 4.1 Embedding model ----------

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# unique id generator

import uuid

def generate_id(prefix: str = ""):
    return f"{prefix}{uuid.uuid4()}"


# json safe parser

def clean_llm_json(text: str):
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text)


# time utility 
def now_utc():
    return datetime.utcnow()


# simple text cleaner 

def now_utc():
    return datetime.utcnow()
import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "MONGODB_URI": os.getenv("MONGO_URI"),
        "MONGODB_DB": os.getenv("MONGODB_DB", "adaptive_prep"),
        "CHROMA_PERSIST": os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
        "PDF_PATH": os.getenv("PDF_PATH"),
        "MCQ_PER_SECTION": int(os.getenv("MCQ_PER_SECTION", 5))
    }
import fitz  # PyMuPDF
import re
from typing import Dict, List

# ---------- 2.1 Raw PDF text extraction ----------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract full text from PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text 
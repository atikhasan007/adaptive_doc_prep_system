import re

# ---------- 2.3 Preprocessing ----------
def preprocess_text(text: str) -> str:
    """Clean extracted text: remove extra whitespace, page markers, etc."""
    # Remove page footer pattern like 'SLATEFALL_DOSSIER.md 2026-05-18\n1 / 50'
    text = re.sub(r'SLATEFALL_DOSSIER\.md\s+\d{4}-\d{2}-\d{2}\s*\n\d+\s*/\s*\d+', '', text)
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.splitlines()]
    return '\n'.join(lines).strip()
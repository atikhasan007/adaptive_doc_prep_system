import fitz  # PyMuPDF
import re
from typing import Dict, List


# ---------- 2.2 Section splitting ----------
def split_into_sections(full_text: str) -> Dict[int, Dict]:
    """
    Split PDF text into numbered sections (1-10).
    Returns: {section_id: {"title": str, "content": str}}

    Strategy: detect 'Section N.' headers in the SLATEFALL dossier.
    """
    # Pattern: "Section 1.", "Section 2.", ... at start of line
    pattern = re.compile(
        r'(?m)^Section\s+(\d+)\.\s+(.+?)$',
        re.IGNORECASE
    )
    matches = list(pattern.finditer(full_text))

    sections = {}
    for i, match in enumerate(matches):
        sec_num   = int(match.group(1))
        sec_title = match.group(2).strip()
        start_pos = match.start()
        end_pos   = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        content   = full_text[start_pos:end_pos].strip()
        sections[sec_num] = {
            "title"  : sec_title,
            "content": content
        }

    return sections
from typing import Dict, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.pdf_processing.preprocessor import preprocess_text
from src.pdf_processing.pdf_loader import extract_text_from_pdf
from src.pdf_processing.section_splitter import split_into_sections
from src.config.config import get_config

config = get_config()

PDF_PATH = config["PDF_PATH"]


# ---------- Run ----------
print(" Extracting PDF text...")
raw_text = extract_text_from_pdf(PDF_PATH)
print(f"   Total chars: {len(raw_text):,}")

print("\n Splitting into sections...")
sections = split_into_sections(raw_text)
for sid, info in sections.items():
    clean = preprocess_text(info["content"])
    sections[sid]["content"] = clean
    print(f"   Section {sid}: '{info['title']}' — {len(clean):,} chars")

print(f"\n Found {len(sections)} sections") 


def build_chunks(sections: Dict[int, Dict]) -> List[Document]:

    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    all_chunks = []

    for sec_id, info in sections.items():

        raw_chunks = splitter.split_text(info["content"])

        for idx, chunk_text in enumerate(raw_chunks):

            doc = Document(
                page_content=chunk_text,
                metadata={
                    "section_id": sec_id,
                    "section_title": info["title"],
                    "chunk_index": idx,
                    "chunk_id": f"sec{sec_id}_chunk{idx}"
                }
            )

            all_chunks.append(doc)

    return all_chunks
from typing import Dict, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


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
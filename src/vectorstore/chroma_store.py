from langchain_chroma import Chroma
from src.embedding.embedder import get_embeddings


def create_vectorstore(all_chunks, persist_dir):

    print(" Embedding chunks and storing in ChromaDB...")

    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=get_embeddings(),
        persist_directory=persist_dir,
        collection_name="slatefall_kb"
    )

    print(" ChromaDB ready")
    print(" Total vectors:", vectorstore._collection.count())

    return vectorstore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.config.config import get_config

config = get_config()

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_vectorstore(all_chunks=None):

    if all_chunks is None:
        return None

    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=get_embeddings(),
        persist_directory=config["CHROMA_PERSIST"],
        collection_name="slatefall_kb"
    )

    print(" ChromaDB Ready")
    return vectorstore
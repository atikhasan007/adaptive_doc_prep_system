
from langchain_chroma import Chroma
from src.config.config import get_config
from src.utils.helper import get_embeddings

config = get_config()



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


from typing import List
from src.database.mongo_client import col_weak_topics, col_sessions, col_questions
from src.vectorstore.chroma_store import create_vectorstore
from src.database.chroma_client import get_vectorstore

vectorstore = get_vectorstore()



def get_weak_topics(section_ids: List[int], top_k: int = 3) -> List[str]:
    """
    Fetch top-K weak topic summaries from MongoDB for given sections.
    Returns list of topic strings for prompt injection.
    """
    pipeline = [
        {"$match": {"section_id": {"$in": section_ids}}},
        {"$sort" : {"wrong_count": -1}},
        {"$limit": top_k},
        {"$project": {"topic_summary": 1, "wrong_count": 1}}
    ]
    results = list(col_weak_topics.aggregate(pipeline))
    return [r["topic_summary"] for r in results]


def get_prior_questions(section_ids: List[int]) -> List[str]:
    """
    Retrieve questions already asked in previous sessions for these sections.
    Used to avoid repetition of mastered questions.
    """
    # Find session IDs for these sections
    session_docs = col_sessions.find(
        {"section_ids": {"$elemMatch": {"$in": section_ids}}},
        {"session_id": 1}
    )
    session_ids = [s["session_id"] for s in session_docs]
    if not session_ids:
        return []

    # Get correct questions (mastered) — avoid repeating these
    q_docs = col_questions.find(
        {"session_id": {"$in": session_ids}, "is_correct": True},
        {"question_text": 1}
    ).limit(20)
    return [q["question_text"] for q in q_docs]







# 🔥 FIXED HERE
def retrieve_context(
    vectorstore,   # ✅ MUST PASS FROM OUTSIDE
    section_ids: List[int],
    query: str = "key facts and concepts",
    k: int = 6
) -> str:

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": {"section_id": {"$in": section_ids}}
        }
    )

    docs = retriever.invoke(query)

    context_parts = []

    for doc in docs:
        header = f"[Section {doc.metadata['section_id']}: {doc.metadata['section_title']}]"
        context_parts.append(f"{header}\n{doc.page_content}")

    return "\n\n".join(context_parts)
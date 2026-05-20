from typing import List , Dict
from src.utils.helper import datetime
from src.database.mongo_client import col_sessions,col_questions,col_weak_topics
from pymongo import DESCENDING



def persist_session(
    section_ids : List[int],
    mcqs        : List[Dict],
    results     : List[Dict],
    session_id  : str = None
) -> str:
    """
    Persist full session to MongoDB:
    - sessions collection: session-level summary
    - questions collection: per-question results
    - weak_topics collection: increment wrong counts
    Returns session_id.
    """
    if session_id is None:
        session_id = str(uuid.uuid4())

    now        = datetime.utcnow()
    correct_n  = sum(1 for r in results if r["is_correct"])
    score_pct  = (correct_n / len(results)) * 100 if results else 0

    # ---- sessions ----
    col_sessions.insert_one({
        "session_id"   : session_id,
        "section_ids"  : section_ids,
        "created_at"   : now,
        "total_q"      : len(results),
        "correct_count": correct_n,
        "score_pct"    : round(score_pct, 2)
    })

    # ---- questions ----
    for r in results:
        col_questions.insert_one({
            "session_id"   : session_id,
            "created_at"   : now,
            **r
        })

    # ---- weak_topics: increment wrong_count ----
    for r in results:
        if not r["is_correct"]:
            col_weak_topics.update_one(
                {
                    "section_id"   : r["section_id"],
                    "topic_summary": r["topic_tag"]
                },
                {
                    "$inc": {"wrong_count": 1},
                    "$set": {"last_wrong_at": now, "section_id": r["section_id"]},
                    "$setOnInsert": {"topic_summary": r["topic_tag"]}
                },
                upsert=True
            )

    print(f"\nSession persisted: {session_id}")
    print(f"   Score: {correct_n}/{len(results)} ({score_pct:.1f}%)")
    return session_id


def export_kb_snapshot(top_n: int = 5) -> Dict:
    """
    Export KB snapshot: top-5 most recent sessions with their question results.
    """
    recent_sessions = list(
        col_sessions.find({}, {"_id": 0})
                    .sort("created_at", DESCENDING)
                    .limit(top_n)
    )
    snapshot = []
    for sess in recent_sessions:
        q_results = list(
            col_questions.find(
                {"session_id": sess["session_id"]},
                {"_id": 0}
            )
        )
        # Convert datetime to string
        for q in q_results:
            if "created_at" in q:
                q["created_at"] = q["created_at"].isoformat()
        sess["created_at"]  = sess["created_at"].isoformat()
        sess["questions"]   = q_results
        snapshot.append(sess)

    return {"kb_snapshot": snapshot, "exported_at": datetime.utcnow().isoformat()}


print("KB persistence functions ready")
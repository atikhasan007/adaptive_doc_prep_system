from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid

from src.pipeline.run_session import run_prep_session
from src.database.mongo_client import (
    col_sessions,
    col_questions,
    col_sections,
    col_weak_topics
)
from src.evaluation.session_eval import score_session

app = FastAPI(title="Adaptive Prep System")


# =========================
# MODELS
# =========================
class StartRequest(BaseModel):
    section_ids: List[int]


class AnswerRequest(BaseModel):
    session_id: str
    answers: Dict[str, str]


# =========================
# START SESSION
# =========================
@app.post("/prep/start")
def start_prep(req: StartRequest):

    try:
        session_id = str(uuid.uuid4())

        result = run_prep_session(
            section_ids=req.section_ids,
            simulate=True
        )

        mcqs = result["mcqs"]

        # SESSION INSERT
        col_sessions.insert_one({
            "session_id": session_id,
            "section_ids": req.section_ids,
            "mcqs": mcqs,
            "results": {}
        })

        # QUESTIONS INSERT
        col_questions.insert_many([
            {
                "session_id": session_id,
                "question_id": q["question_id"],
                "topic": q.get("topic", "general"),
                "is_correct": None
            }
            for q in mcqs
        ])

        # SECTIONS UPDATE
        for sid in req.section_ids:
            col_sections.update_one(
                {"section_id": sid},
                {"$inc": {"total_attempts": 1}},
                upsert=True
            )

        return {
            "session_id": session_id,
            "mcqs": mcqs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# SUBMIT ANSWERS
# =========================
@app.post("/prep/submit")
def submit_answers(req: AnswerRequest):

    session = col_sessions.find_one({"session_id": req.session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    mcqs = session["mcqs"]

    results = score_session(mcqs, req.answers)

    # =========================
    # SAFE NORMALIZATION (IMPORTANT FIX)
    # =========================
    if isinstance(results, list):
        details = results
        correct_count = sum(1 for x in results if x.get("is_correct"))
    else:
        details = results.get("details", [])
        correct_count = results.get("correct_count", 0)

    # =========================
    # UPDATE SESSION
    # =========================
    col_sessions.update_one(
        {"session_id": req.session_id},
        {"$set": {"results": results}}
    )

    # =========================
    # UPDATE QUESTIONS + WEAK TOPICS
    # =========================
    for item in details:

        qid = item.get("question_id")
        is_correct = item.get("is_correct", False)
        topic = item.get("topic", "general")

        if qid:
            col_questions.update_one(
                {"session_id": req.session_id, "question_id": qid},
                {"$set": {"is_correct": is_correct}}
            )

        if not is_correct:
            col_weak_topics.update_one(
                {"topic": topic},
                {"$inc": {"wrong_count": 1}},
                upsert=True
            )

    # =========================
    # UPDATE SECTIONS
    # =========================
    section_ids = session["section_ids"]

    for sid in section_ids:
        col_sections.update_one(
            {"section_id": sid},
            {"$inc": {
                "total_attempts": 1,
                "total_correct": correct_count
            }},
            upsert=True
        )

    return {
        "session_id": req.session_id,
        "results": results
    }


# =========================
# GET RESULT
# =========================
@app.get("/prep/result/{session_id}")
def get_result(session_id: str):

    session = col_sessions.find_one(
        {"session_id": session_id},
        {"_id": 0}
    )

    if not session:
        raise HTTPException(status_code=404, detail="Not found")

    return session
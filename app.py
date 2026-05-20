from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid

from src.pipeline.run_session import run_prep_session
from src.database.mongo_client import col_sessions

app = FastAPI(title="Adaptive Prep System")


# =========================
# SAFE GETTERS
# =========================
def get_question(q: dict):
    return (
        q.get("question_text")
        or q.get("question")
        or q.get("text")
        or q.get("stem")
        or "No question available"
    )


def get_options(q: dict):
    return q.get("options", {})


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
        result = run_prep_session(
            section_ids=req.section_ids,
            simulate=False
        )

        session_id = result["session_id"]
        mcqs = result["mcqs"]

        col_sessions.insert_one({
            "session_id": session_id,
            "section_ids": req.section_ids,
            "mcqs": mcqs,
            "results": None
        })

        return {
            "session_id": session_id,
            "mcqs": mcqs
        }

    except Exception as e:
        print("❌ START ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# SUBMIT (FULL SAFE FIX)
# =========================
@app.post("/prep/submit")
def submit_answers(req: AnswerRequest):

    session = col_sessions.find_one({"session_id": req.session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    mcqs = session.get("mcqs", [])

    results = []
    correct = 0

    for q in mcqs:

        qid = q.get("question_id")
        user_ans = req.answers.get(qid)

        correct_ans = q.get("correct_answer")

        is_correct = (user_ans == correct_ans)

        if is_correct:
            correct += 1

        results.append({
            "question_id": qid,
            "question": get_question(q),   # 🔥 SAFE FIX HERE
            "options": get_options(q),
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    total = len(results)

    final_result = {
        "total_questions": total,
        "correct_answers": correct,
        "score_percentage": round((correct / total) * 100, 2) if total else 0,
        "results": results
    }

    col_sessions.update_one(
        {"session_id": req.session_id},
        {"$set": {"results": final_result}}
    )

    return {
        "session_id": req.session_id,
        "results": final_result
    }


# =========================
# GET RESULT
# =========================
@app.get("/prep/result/{session_id}")
def get_result(session_id: str):

    session = col_sessions.find_one({"session_id": session_id}, {"_id": 0})

    if not session:
        raise HTTPException(status_code=404, detail="Not found")

    return session
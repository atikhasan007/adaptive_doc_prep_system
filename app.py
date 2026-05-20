from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import uuid
import traceback

from src.pipeline.run_session import run_prep_session
from src.database.mongo_client import col_sessions, col_questions, col_sections, col_weak_topics
from src.evaluation.session_eval import score_session

app = FastAPI(title="Adaptive Prep System")


class StartRequest(BaseModel):
    section_ids: List[int]


class AnswerRequest(BaseModel):
    session_id: str
    answers: Dict[str, str]


@app.get("/")
def home():
    return {"status": "running"}


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

        mcqs = result.get("mcqs", [])

        # SESSION SAVE
        col_sessions.insert_one({
            "session_id": session_id,
            "section_ids": req.section_ids,
            "mcqs": mcqs,
            "results": {}
        })

        # QUESTIONS TRACKING
        col_questions.insert_many([
            {
                "session_id": session_id,
                "question_id": q.get("question_id"),
                "topic": q.get("topic_tag", "general"),
                "is_correct": None
            }
            for q in mcqs
        ])

        return {
            "session_id": session_id,
            "mcqs": mcqs
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# SUBMIT ANSWERS
# =========================
@app.post("/prep/submit")
def submit_answers(req: AnswerRequest):

    session = col_sessions.find_one({"session_id": req.session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    mcqs = session.get("mcqs", [])

    results = score_session(mcqs, req.answers)

    col_sessions.update_one(
        {"session_id": req.session_id},
        {"$set": {"results": results}}
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

    session = col_sessions.find_one({"session_id": session_id}, {"_id": 0})

    if not session:
        raise HTTPException(status_code=404, detail="Not found")

    return session


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
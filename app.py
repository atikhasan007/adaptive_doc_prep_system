from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

import uvicorn

from src.pipeline.run_session import run_prep_session
from src.database.mongo_client import col_sessions
from src.evaluation.session_eval import score_session


app = FastAPI(title="Adaptive Document Prep System")


# =========================
# MODELS
# =========================
class StartRequest(BaseModel):
    section_ids: List[int]


class AnswerRequest(BaseModel):
    session_id: str
    answers: Dict[str, str]


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {
        "status": "running",
        "service": "Adaptive Prep API"
    }


# =========================
# START SESSION
# =========================
@app.post("/prep/start")
def start_prep(req: StartRequest):

    try:
        result = run_prep_session(
            section_ids=req.section_ids,
            simulate=True
        )

        if not result or "session_id" not in result:
            raise HTTPException(status_code=500, detail="Invalid pipeline response")

        session_data = {
            "session_id": result["session_id"],
            "section_ids": req.section_ids,
            "mcqs": result.get("mcqs", []),
            "results": {}
        }

        col_sessions.insert_one(session_data)

        return {
            "session_id": result["session_id"],
            "mcqs": result.get("mcqs", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# SUBMIT ANSWERS
# =========================
@app.post("/prep/submit")
def submit_answers(req: AnswerRequest):

    try:
        session = col_sessions.find_one({"session_id": req.session_id})

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        mcqs = session.get("mcqs", [])

        if not mcqs:
            raise HTTPException(status_code=400, detail="MCQs missing")

        answers = req.answers or {}

        results = score_session(mcqs, answers)

        col_sessions.update_one(
            {"session_id": req.session_id},
            {"$set": {"results": results}}
        )

        return {
            "session_id": req.session_id,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
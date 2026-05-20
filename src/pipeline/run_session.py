
from typing import List, Dict
from src.database.mongo_client import col_sessions
from src.prompts.mcq_prompt import generate_mcqs, MCQ_PER_SECTION 
from src.utils.helper import uuid
import os
import json
from src.evaluation.session_eval import simulate_answers ,score_session
from src.export.kb_persistence import export_kb_snapshot, persist_session
from src.evaluation.session_eval import collect_answers_interactive


def run_prep_session(
    section_ids  : List[int],
    simulate     : bool = True,
    correct_rate : float = 0.6,
    output_dir   : str = None
) -> Dict:
    """
    Master orchestrator — runs one full prep session:

    1. Check KB for prior history  (adaptive detection)
    2. Generate MCQs               (adaptive if returning user)
    3. Collect answers             (simulated or interactive)
    4. Score session
    5. Persist to MongoDB KB
    6. Export snapshot
    7. Save outputs if output_dir given

    Returns: {session_id, mcqs, results, snapshot}
    """
    session_id = str(uuid.uuid4())
    print(f"\n{'#'*60}")
    print(f"PREP SESSION: {session_id[:8]}...")
    print(f"   Sections : {section_ids}")
    print(f"   Mode     : {'SIMULATED' if simulate else 'INTERACTIVE'}")
    print(f"{'#'*60}")

    # STEP 1: Check for prior history
    prior_count = col_sessions.count_documents(
        {"section_ids": {"$elemMatch": {"$in": section_ids}}}
    )
    is_adaptive = prior_count > 0
    print(f"\n Prior sessions found: {prior_count}")
    print(f"   Adaptive mode: {'ON' if is_adaptive else 'OFF (first run)'}")

    # STEP 2: Generate MCQs
    mcqs = generate_mcqs(
        section_ids=section_ids,
        n_per_section=MCQ_PER_SECTION,
        is_adaptive=is_adaptive
    )

    # STEP 3: Collect answers
    if simulate:
        print(f"\nSimulating answers (correct rate: {correct_rate*100:.0f}%)")
        user_answers = simulate_answers(mcqs, correct_rate=correct_rate)
    else:
        user_answers = collect_answers_interactive(mcqs)

    # STEP 4: Score
    results = score_session(mcqs, user_answers)

    # STEP 5: Persist KB
    persist_session(section_ids, mcqs, results, session_id=session_id)

    # STEP 6: Export snapshot
    snapshot = export_kb_snapshot(top_n=5)

    # STEP 7: Save output files
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        q_path  = os.path.join(output_dir, "questions.json")
        kb_path = os.path.join(output_dir, "kb_snapshot.json")

        with open(q_path, "w", encoding="utf-8") as f:
            json.dump({"session_id": session_id, "mcqs": mcqs, "results": results}, f, indent=2, default=str)
        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, default=str)

        print(f"\n Outputs saved:")
        print(f"   {q_path}")
        print(f"   {kb_path}")

    return {
        "session_id": session_id,
        "mcqs"      : mcqs,
        "results"   : results,
        "snapshot"  : snapshot
    }


print(" Master orchestrator ready")
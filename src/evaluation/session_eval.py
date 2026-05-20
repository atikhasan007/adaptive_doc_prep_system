import random
from typing import List , Dict




def present_question(mcq: Dict) -> None:
    """Pretty-print a single MCQ."""
    print(f"\n{'='*60}")
    print(f"Q{mcq['question_id']}: {mcq['question_text']}")
    for key, val in mcq["options"].items():
        print(f"   {key}) {val}")


def collect_answers_interactive(mcqs: List[Dict]) -> Dict[str, str]:
    """
    Collect real user answers via input().
    Returns {question_id: user_answer}
    """
    user_answers = {}
    for mcq in mcqs:
        present_question(mcq)
        while True:
            ans = input("Your answer (A/B/C/D): ").strip().upper()
            if ans in ["A", "B", "C", "D"]:
                user_answers[mcq["question_id"]] = ans
                break
            print("Please enter A, B, C, or D")
    return user_answers


def simulate_answers(mcqs: List[Dict], correct_rate: float = 0.6) -> Dict[str, str]:
    """
    Simulate user answers with a given correct rate.
    Used for automated scenario evaluation.
    """
    simulated = {}
    options   = ["A", "B", "C", "D"]
    for mcq in mcqs:
        if random.random() < correct_rate:
            simulated[mcq["question_id"]] = mcq["correct_answer"]
        else:
            wrong_opts = [o for o in options if o != mcq["correct_answer"]]
            simulated[mcq["question_id"]] = random.choice(wrong_opts)
    return simulated


def score_session(
    mcqs        : List[Dict],
    user_answers: Dict[str, str]
) -> List[Dict]:
    """
    Score each MCQ against the user's answer.
    Returns list of result dicts.
    Prints feedback for wrong answers.
    """
    results    = []
    correct_n  = 0

    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)

    for mcq in mcqs:
        qid        = mcq["question_id"]
        user_ans   = user_answers.get(qid, "")
        correct    = mcq["correct_answer"]
        is_correct = user_ans == correct

        if is_correct:
            correct_n += 1
            status = "CORRECT"
        else:
            status = f"WRONG  (You: {user_ans} | Correct: {correct})"

        print(f"\n{qid}: {mcq['question_text'][:80]}...")
        print(f"   {status}")
        if not is_correct:
            print(f"Explanation: {mcq['explanation']}")

        results.append({
            "question_id"   : qid,
            "question_text" : mcq["question_text"],
            "options"       : mcq["options"],
            "correct_answer": correct,
            "user_answer"   : user_ans,
            "is_correct"    : is_correct,
            "explanation"   : mcq["explanation"],
            "section_id"    : mcq.get("section_id"),
            "topic_tag"     : mcq.get("topic_tag", "")
        })

    score_pct = (correct_n / len(mcqs)) * 100
    print(f"\n{'='*60}")
    print(f"Score: {correct_n}/{len(mcqs)} ({score_pct:.1f}%)")
    print("="*60)

    return results


print("Evaluation functions ready")
import json
import google.generativeai as genai
import re
from typing import List, Dict
from src.config.config import get_config
from src.retrieval.retrieval_engine import retrieve_context , get_weak_topics, get_prior_questions
from src.database.chroma_client import get_vectorstore

vectorstore = get_vectorstore()



config = get_config()
MCQ_PER_SECTION = config["MCQ_PER_SECTION"]
genai.configure(api_key=config["GEMINI_API_KEY"])

llm_model = genai.GenerativeModel("gemini-3.1-flash-lite")


def build_mcq_prompt(
    context       : str,
    section_ids   : List[int],
    n_questions   : int,
    weak_topics   : List[str] = None,
    prior_questions: List[str] = None,
    is_adaptive   : bool = False
) -> str:
    """
    Build the MCQ generation prompt with optional adaptive context.
    """
    sections_str = ", ".join(str(s) for s in section_ids)

    adaptive_block = ""
    if is_adaptive:
        if weak_topics:
            topics_str = "\n".join(f"  - {t}" for t in weak_topics)
            adaptive_block += f"""
ADAPTIVE INSTRUCTION:
The user has previously struggled with the following topics. 
Prioritize generating questions on these weak areas:
{topics_str}
"""
        if prior_questions:
            prior_str = "\n".join(f"  - {q}" for q in prior_questions[:5])
            adaptive_block += f"""
AVOID REPEATING these already-mastered questions:
{prior_str}
"""

    prompt = f"""You are an expert exam question generator.

SOURCE CONTEXT (from Sections {sections_str}):
{context}

{adaptive_block}

TASK:
Generate exactly {n_questions} Multiple Choice Questions (MCQs) from the context above.

RULES:
1. Each question must have exactly 4 answer options labeled A, B, C, D.
2. Only one option is correct.
3. Include a concise explanation (1-2 sentences) for the correct answer.
4. Questions must be factual and directly answerable from the context.
5. Vary difficulty: mix easy, medium, hard questions.
6. Return ONLY valid JSON. No extra text before or after.

OUTPUT FORMAT (strict JSON array):
[
  {{
    "question_id"  : "q1",
    "question_text": "<question>",
    "options"      : {{"A": "<opt>", "B": "<opt>", "C": "<opt>", "D": "<opt>"}},
    "correct_answer": "A",
    "explanation"  : "<why this answer is correct>",
    "section_id"   : {section_ids[0]},
    "topic_tag"    : "<short topic label>"
  }}
]
"""
    return prompt


def generate_mcqs(
    section_ids    : List[int],
    n_per_section  : int = MCQ_PER_SECTION,
    is_adaptive    : bool = False
) -> List[Dict]:
    """
    Full MCQ generation pipeline:
    1. Retrieve context from ChromaDB
    2. Get weak topics + prior questions from MongoDB (if adaptive)
    3. Build prompt and call Gemini
    4. Parse and return MCQ list
    """
    total_q = n_per_section * len(section_ids)
    print(f"\n Generating {total_q} MCQs for sections {section_ids}...")

    # Retrieve context
    context = retrieve_context(vectorstore, section_ids, k=8)

    # Adaptive memory
    weak_topics    = get_weak_topics(section_ids) if is_adaptive else []
    prior_qs       = get_prior_questions(section_ids) if is_adaptive else []

    if is_adaptive:
        print(f"Adaptive mode ON — weak topics: {weak_topics}")

    # Build prompt
    prompt = build_mcq_prompt(
        context=context,
        section_ids=section_ids,
        n_questions=total_q,
        weak_topics=weak_topics,
        prior_questions=prior_qs,
        is_adaptive=is_adaptive
    )

    # Call Gemini
    response  = llm_model.generate_content(prompt)
    raw_text  = response.text.strip()

    # Parse JSON (strip markdown fences if present)
    raw_text  = re.sub(r'^```json\s*', '', raw_text)
    raw_text  = re.sub(r'\s*```$', '', raw_text)
    mcqs      = json.loads(raw_text)

    # Assign unique IDs
    for i, q in enumerate(mcqs):
        q["question_id"] = f"q{i+1}"

    print(f" Generated {len(mcqs)} MCQs")
    return mcqs


print("MCQ engine ready")
import json
import re
import google.generativeai as genai

from typing import List, Dict

from src.prompts.mcq_prompt import build_mcq_prompt
from src.retrieval.retrieval_engine import (
    retrieve_context,
    get_weak_topics,
    get_prior_questions
)

from src.config.config import get_config

config = get_config()

genai.configure(api_key=config["GEMINI_API_KEY"])
llm_model = genai.GenerativeModel("gemini-3.1-flash-lite")


def generate_mcqs(
    section_ids    : List[int],
    n_per_section  : int,
    is_adaptive    : bool = False
) -> List[Dict]:

    total_q = n_per_section * len(section_ids)

    print(f"\n Generating {total_q} MCQs for sections {section_ids}...")

    # Retrieve context
    context = retrieve_context(section_ids, k=8)

    # Adaptive memory
    weak_topics = get_weak_topics(section_ids) if is_adaptive else []
    prior_qs = get_prior_questions(section_ids) if is_adaptive else []

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
    response = llm_model.generate_content(prompt)
    raw_text = response.text.strip()

    # Clean JSON
    raw_text = re.sub(r'^```json\s*', '', raw_text)
    raw_text = re.sub(r'\s*```$', '', raw_text)

    mcqs = json.loads(raw_text)

    # Add IDs
    for i, q in enumerate(mcqs):
        q["question_id"] = f"q{i+1}"

    print(f" Generated {len(mcqs)} MCQs")

    return mcqs


print("MCQ engine ready")
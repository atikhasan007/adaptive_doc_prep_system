import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Adaptive Prep System", layout="wide")

st.title("📘 Adaptive Document Prep System")


# =========================
# STATE
# =========================
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None


# =========================
# START
# =========================
st.header("1️⃣ Start Session")

sections = st.multiselect("Select Sections", list(range(1, 11)))

if st.button("Generate MCQs"):

    res = requests.post(
        f"{API_URL}/prep/start",
        json={"section_ids": sections}
    )

    if res.status_code == 200:
        data = res.json()
        st.session_state.session_id = data["session_id"]
        st.session_state.mcqs = data["mcqs"]
        st.success("MCQs Generated!")
    else:
        st.error(res.text)


# =========================
# ANSWER
# =========================
if st.session_state.mcqs:

    st.header("2️⃣ Answer Questions")

    answers = {}

    for i, q in enumerate(st.session_state.mcqs, start=1):

        question = (
            q.get("question_text")
            or q.get("question")
            or q.get("text")
            or q.get("stem")
        )

        st.markdown(f"### ❓ Q{i}: {question}")

        options = q.get("options", {})

        ans = st.radio(
            "Select answer",
            list(options.keys()),
            format_func=lambda x: f"{x}: {options[x]}",
            key=f"q_{i}"
        )

        answers[q["question_id"]] = ans

        st.markdown("---")

    if st.button("📤 Submit Answers"):

        res = requests.post(
            f"{API_URL}/prep/submit",
            json={
                "session_id": st.session_state.session_id,
                "answers": answers
            }
        )

        if res.status_code == 200:

            data = res.json()["results"]

            st.success("Result Ready 🎉")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total", data["total_questions"])
            col2.metric("Correct", data["correct_answers"])
            col3.metric("Score", f"{data['score_percentage']}%")

            st.markdown("---")
            st.subheader("📝 Review")

            for idx, item in enumerate(data["results"], start=1):

                with st.container(border=True):

                    st.markdown(f"### Q{idx}: {item['question']}")

                    if item["is_correct"]:
                        st.success("Correct")
                    else:
                        st.error("Wrong")

                    st.markdown(f"Your Answer: `{item['user_answer']}`")
                    st.markdown(f"Correct Answer: `{item['correct_answer']}`")

                    if item["explanation"]:
                        with st.expander("Explanation"):
                            st.write(item["explanation"])

        else:
            st.error(res.text)
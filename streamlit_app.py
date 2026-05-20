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
# START SESSION
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
# ANSWER MCQS
# =========================
if st.session_state.mcqs:

    st.header("2️⃣ Answer Questions")

    answers = {}

    for i, q in enumerate(st.session_state.mcqs):

        st.subheader(q["question_text"])

        ans = st.radio(
            "Select answer",
            ["A", "B", "C", "D"],
            key=f"q_{i}"
        )

        answers[q["question_id"]] = ans

    if st.button("Submit Answers"):

        res = requests.post(
            f"{API_URL}/prep/submit",
            json={
                "session_id": st.session_state.session_id,
                "answers": answers
            }
        )

        if res.status_code == 200:
            st.success("Results Saved")
            st.json(res.json()["results"])
        else:
            st.error(res.text)


# =========================
# LOAD RESULT
# =========================
st.markdown("---")

if st.button("Load Result"):

    if st.session_state.session_id:

        res = requests.get(
            f"{API_URL}/prep/result/{st.session_state.session_id}"
        )

        st.json(res.json())
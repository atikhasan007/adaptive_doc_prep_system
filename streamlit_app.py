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

    if not sections:
        st.error("Select sections first")
    else:
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
# SHOW MCQS
# =========================
if st.session_state.mcqs:

    st.header("2️⃣ MCQs")

    answers = {}

    for i, q in enumerate(st.session_state.mcqs):

        st.subheader(q.get("question_text", ""))

        options = q.get("options", {})

        st.write("A:", options.get("A"))
        st.write("B:", options.get("B"))
        st.write("C:", options.get("C"))
        st.write("D:", options.get("D"))

        answers[q["question_id"]] = st.radio(
            "Answer",
            ["A", "B", "C", "D"],
            key=i
        )

    if st.button("Submit Answers"):

        res = requests.post(
            f"{API_URL}/prep/submit",
            json={
                "session_id": st.session_state.session_id,
                "answers": answers
            }
        )

        if res.status_code == 200:
            st.success("Submitted Successfully")
            st.json(res.json()["results"])
        else:
            st.error(res.text)


# =========================
# LOAD RESULT
# =========================
if st.button("Load Result"):

    if st.session_state.session_id:

        res = requests.get(
            f"{API_URL}/prep/result/{st.session_state.session_id}"
        )

        st.json(res.json())

    else:
        st.warning("Start session first")
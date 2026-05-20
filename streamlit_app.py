import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="Adaptive Prep System", layout="wide")

st.title("📘 Adaptive Document Prep System")


# =========================
# SESSION STATE INIT
# =========================
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None


# =========================
# STEP 1: SECTION SELECT
# =========================
st.header("1️⃣ Select Sections")

sections = st.multiselect(
    "Choose sections (1-10)",
    list(range(1, 11))
)

if st.button("Start Prep"):

    if not sections:
        st.error("Please select at least one section")
    else:
        try:
            res = requests.post(
                f"{API_URL}/prep/start",
                json={"section_ids": sections}
            )

            if res.status_code == 200:
                data = res.json()

                st.session_state.session_id = data["session_id"]
                st.session_state.mcqs = data["mcqs"]

                st.success("MCQs Generated Successfully!")
            else:
                st.error(res.text)

        except Exception as e:
            st.error(f"Request failed: {str(e)}")

# =========================
# STEP 2: SHOW MCQS (FIXED)
# =========================
if st.session_state.mcqs:

    st.header("2️⃣ Answer MCQs")

    # store answers & results
    if "feedback" not in st.session_state:
        st.session_state.feedback = {}

    for i, q in enumerate(st.session_state.mcqs):

        st.subheader(f"Q{i+1}: {q['question_text']}")

        st.write("A:", q["options"]["A"])
        st.write("B:", q["options"]["B"])
        st.write("C:", q["options"]["C"])
        st.write("D:", q["options"]["D"])

        selected = st.radio(
            "Select answer",
            ["A", "B", "C", "D"],
            key=f"q_{i}"
        )

        # per-question submit
        if st.button(f"Submit Q{i+1}", key=f"submit_{i}"):

            correct = q["correct_answer"]

            if selected == correct:
                st.success("✅ Correct Answer!")
                st.session_state.feedback[q["question_id"]] = {
                    "status": "correct"
                }
            else:
                st.error("❌ Wrong Answer!")

                st.info(f"""
                💡 **Explanation:**  
                {q.get('explanation', 'No explanation available')}
                """)

                st.session_state.feedback[q["question_id"]] = {
                    "status": "wrong",
                    "correct_answer": correct,
                    "your_answer": selected,
                    "explanation": q.get("explanation", "")
                }

        st.markdown("---")
# =========================
# STEP 3: LOAD PREVIOUS RESULT
# =========================
st.markdown("---")

if st.button("📊 Load Previous Result"):

    if st.session_state.session_id:

        try:
            res = requests.get(
                f"{API_URL}/prep/result/{st.session_state.session_id}"
            )

            if res.status_code == 200:

                st.header("📊 Saved Result")
                st.json(res.json())

            else:
                st.error(res.text)

        except Exception as e:
            st.error(f"Failed: {str(e)}")

    else:
        st.warning("No session found. Start prep first.")
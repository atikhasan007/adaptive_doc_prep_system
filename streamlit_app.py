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

    st.header("📝 MCQ Exam")

    answers = {}

    for i, q in enumerate(st.session_state.mcqs):

        st.markdown("---")

        question = q.get("question_text", "No Question")

        options = q.get("options", {})

        st.markdown(f"### Q{i+1}. {question}")

        answers[q["question_id"]] = st.radio(
            "Select Answer",
            [
                f"A. {options.get('A', '')}",
                f"B. {options.get('B', '')}",
                f"C. {options.get('C', '')}",
                f"D. {options.get('D', '')}",
            ],
            key=f"q_{i}"
        )[0]

    st.markdown("")

    # =========================
    # SUBMIT ANSWERS
    # =========================
    if st.button("✅ Submit Answers", use_container_width=True):

        with st.spinner("Checking Answers..."):

            res = requests.post(
                f"{API_URL}/prep/submit",
                json={
                    "session_id": st.session_state.session_id,
                    "answers": answers
                }
            )

        if res.status_code == 200:

            st.success("🎉 Answers Submitted Successfully!")

            data = res.json()
            results = data.get("results", [])

            if results:

                st.markdown("---")
                st.header("📊 Results")

                correct_count = 0

                for i, r in enumerate(results):

                    st.markdown(f"## Q{i+1}")

                    st.write(r.get("question_text", ""))

                    options = r.get("options", {})

                    st.write(f"🅰️ A: {options.get('A', '')}")
                    st.write(f"🅱️ B: {options.get('B', '')}")
                    st.write(f"🇨 C: {options.get('C', '')}")
                    st.write(f"🇩 D: {options.get('D', '')}")

                    st.write(
                        f"🧑 Your Answer: {r.get('user_answer', '')}"
                    )

                    st.write(
                        f"✅ Correct Answer: {r.get('correct_answer', '')}"
                    )

                    if r.get("is_correct"):

                        st.success("Correct Answer ✅")
                        correct_count += 1

                    else:

                        st.error("Wrong Answer ❌")

                    st.info(
                        f"💡 Explanation: {r.get('explanation', '')}"
                    )

                    st.markdown("---")

                total_questions = len(results)

                st.metric(
                    "🎯 Final Score",
                    f"{correct_count}/{total_questions}"
                )

            else:
                st.warning("No Results Found")

        else:
            st.error(res.text)



            #md

## Adaptive Document Preparation System


## fast work 
- research  
then
- module codding



##  1. project setup 
conda create -n assignment_ai_ml python=3.10

conda activate assignment_ai_ml

pip install -r requirements.txt

##  2. project over view

This system enables intelligent exam preparation by:

- Generating MCQs from selected document sections using an LLM
- Evaluating user responses automatically
- Storing session history in a Knowledge Base (KB)
- Detecting weak topics from past performance
- Adapting future MCQs based on user weaknesses



##  3. Business Objectives
Traditional learning systems are static and repetitive.

This project solves that problem by introducing **adaptive learning intelligence**:

- Dynamic MCQ generation based on user history
- Weak-area detection from past mistakes
- Continuous improvement of question quality
- Personalized exam preparation experience



##  4. Data Source
given assigenment : SLATEFALL_DOSSIER.pdf



##  5. Models Used and api for llm
gemeni api 
model : gemini-3.1-flash-lite
embedding model : sentence-transformers/all-MiniLM-L6-v2


##  6. End-to-End Application workflow
1. config
2. database
3. utils
4. pdf_processing
5. embedding
6. vector store
7. retreval
8. llm
9. prompts
10. evaluation
11. export
12. pipeline
13. demo.py for check
14. app.py
15. steamlit.py

## 7. Adaptive Learning Flow
  User selects sections
        ↓
Retrieve PDF context (ChromaDB)
        ↓
Check previous performance (MongoDB)
        ↓
Detect weak topics
        ↓
Generate MCQs (Gemini + adaptive prompt)
        ↓
User answers
        ↓
Score evaluation
        ↓
Store results in KB
        ↓
Update weak topics
        ↓
Next session becomes smarter

---

## 8. Database Design

### 📌 ChromaDB
- Used for semantic search
- Stores embedded document chunks
- Retrieves relevant context for MCQ generation

### 📌 MongoDB
- Stores:
  - Sessions
  - Questions
  - User answers
  - Scores
  - Weak topics (knowledge base)

---

## 9. Tech Stack
- Python
- FastAPI
- Streamlit
- MongoDB
- ChromaDB
- Gemini API
- Sentence Transformers

## 10. Key Features
- Adaptive MCQ generation
- Weak topic detection
- Session-based learning history
- Real-time scoring system
- Vector-based document retrieval
- LLM-powered question generation


##  11. How to Run This Project
- 1. clone the repository
git clone https://github.com/atikhasan007/adaptive_doc_prep_system.git

- 2. Backend Run (FastAPI)
- uvicorn app:app --reload

- 3. Streamlit UI Run
- streamlit run streamlit_app.py


##  12. Author & Contact 
Md Atik Hasan
Email : imatik513@gmail.com
Phone : +8801827693853




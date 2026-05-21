
## Adaptive Document Preparation System


## fast work 
- research  
then
- module codding
- and test demo.py file
- logger file include  utils  file 



##  1. project setup 
conda create -n assignment_ai_ml python=3.10

conda activate assignment_ai_ml

pip install -r requirements.txt

🧠 Overview

The Adaptive Document Preparation System is an AI-powered backend application that transforms static study material into a personalized learning system.

It:

- Ingests a multi-section PDF document
- Generates MCQs using an LLM
- Evaluates user responses automatically
- Stores session history in a Knowledge Base (KB)
- Adapts future questions based on user weaknesses

👉 The key innovation is history-aware adaptive MCQ generation.


##  3. Business Objectives
Traditional learning systems are static and repetitive.
This system introduces adaptive intelligence:

- Dynamic MCQ generation from selected sections
- Automatic evaluation and feedback
- Weak-topic detection from past performance
- Personalized question selection in future sessions
- Continuous improvement of learning effectiveness



##  4. Data Source
given assigenment : SLATEFALL_DOSSIER.pdf



##  5. Models Used and api for llm
- gemeni api 
- model : gemini-3.1-flash-lite
  
- Hugging Face 
- embedding model : sentence-transformers/all-MiniLM-L6-v2


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

- User selects sections
        ↓
- Retrieve PDF context (ChromaDB)
        ↓
- Check previous performance (MongoDB)
        ↓
- Detect weak topics
        ↓
- Generate MCQs (Gemini + adaptive prompt)
        ↓
- User answers
        ↓
- Score evaluation
        ↓
- Store results in KB
        ↓
- Update weak topics
        ↓
- Next session becomes smarter



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


## Explicit Adaptive Algorithm

Example needed:
weak_topic_score = wrong_count / total_attempts
sampling weight in MCQ generation prompt



##  11. How to Run This Project
- 1. clone the repository * git clone https://github.com/atikhasan007/adaptive_doc_prep_system.git

- 2. Backend Run (FastAPI) * uvicorn app:app --reload

- 3. Streamlit UI Run  * streamlit run streamlit_app.py


##  12. Author & Contact 
Md Atik Hasan
Email : imatik513@gmail.com
Phone : +8801827693853

## project UI overview and other UI 
--
<img width="1910" height="1012" alt="report 1" src="https://github.com/user-attachments/assets/66a71130-397e-4932-ab9a-5fe07bc4f70a" />
<img width="1917" height="966" alt="report 2" src="https://github.com/user-attachments/assets/60892004-920c-4c37-bb4b-497a11a11d7c" />
<img width="1907" height="722" alt="report 3" src="https://github.com/user-attachments/assets/40330021-fba8-435f-91ec-6aadc62ad335" />
<img width="1917" height="690" alt="report 4" src="https://github.com/user-attachments/assets/60d4d2c0-7f71-4130-8b29-e14c3ad52a06" />
<img width="1917" height="690" alt="report 5" src="https://github.com/user-attachments/assets/d114e3ee-42bb-4b07-84a9-4196c51b1436" />
<img width="1911" height="337" alt="report 6" src="https://github.com/user-attachments/assets/bd260044-b1ff-46da-865d-0d3ed2454c0a" />
<img width="1817" height="652" alt="report 7" src="https://github.com/user-attachments/assets/e56a8177-9d11-4099-9f14-23c85fc0b65d" />
<img width="1877" height="722" alt="report 8" src="https://github.com/user-attachments/assets/9bcfd0f7-d5b5-4a7f-974c-8c783c9d2d47" />
<img width="1902" height="827" alt="report 9" src="https://github.com/user-attachments/assets/cbc5b09e-5622-4dd1-9a56-65a1ebfdfcc7" />









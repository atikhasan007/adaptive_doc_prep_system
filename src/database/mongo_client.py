from pymongo import MongoClient
from src.config.config import get_config

config = get_config()

client = MongoClient(config["MONGODB_URI"])
db = client[config["MONGODB_DB"]]

print(" MongoDB Connected")

# ================= COLLECTIONS =================
col_sections = db["sections"]
col_sessions = db["sessions"]
col_questions = db["questions"]
col_weak_topics = db["weak_topics"]

# ================= INDEXES =================
col_sections.create_index("section_id", unique=True)

col_sessions.create_index([
    ("section_ids", 1),
    ("created_at", -1)
])

col_questions.create_index([
    ("session_id", 1),
    ("is_correct", 1)
])

col_weak_topics.create_index([
    ("section_id", 1),
    ("wrong_count", -1)
])

print(" Mongo Indexes Ready")
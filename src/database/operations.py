from datetime import datetime
from src.database.mongo_client import col_sections   # ✅ ONLY THIS


def store_sections(sections: dict):

    print(" Storing sections...")

    for sec_id, info in sections.items():
        col_sections.update_one(
            {"section_id": sec_id},
            {"$set": {
                "section_id": sec_id,
                "title": info["title"],
                "content": info["content"],
                "char_count": len(info["content"]),
                "indexed_at": datetime.utcnow()
            }},
            upsert=True
        )

    print(" Sections stored successfully")
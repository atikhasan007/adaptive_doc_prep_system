


# # logger system check 

# from src.utils.logger import get_logger

# logger = get_logger("pdf_processing")

# logger.info("PDF loading started")





# from src.utils.logger import get_logger
# from src.config.config import get_config

# # ================= LOGGER =================
# logger = get_logger("demo")

# logger.info("System starting...")

# # ================= CONFIG =================
# config = get_config()

# logger.info("Config Loaded Successfully")

# logger.info(f"PDF Path: {config['PDF_PATH']}")
# logger.info(f"DB Name: {config['MONGODB_DB']}")
# logger.info(f"Chroma Path: {config['CHROMA_PERSIST']}")
# logger.info(f"MCQ per section: {config['MCQ_PER_SECTION']}")

# logger.info("Demo setup completed successfully")






# from src.database.operations import store_sections

# sections = { 
#     1: {"title": "AI", "content": "Artificial Intelligence basics"},
#     2: {"title": "ML", "content": "Machine Learning basics"}
# }

# store_sections(sections)

# print(" DEMO RUN SUCCESSFUL")




# from src.utils.logger import get_logger

# logger = get_logger("demo")

# try:
#     from src.pipeline.run_session import run_prep_session

#     logger.info("Starting Scenario A")

#     result_a = run_prep_session(
#         section_ids=[1, 2],
#         simulate=True,
#         correct_rate=0.5,
#         output_dir="outputss/scenario_a"
#     )

#     logger.info("Scenario A complete")

# except Exception as e:
#     logger.exception("ERROR OCCURRED IN DEMO RUN")






# from src.utils.logger import get_logger

# logger = get_logger("demo")

# try:
#     from src.pipeline.run_session import run_prep_session

#     logger.info("Starting Scenario B")

#     result_b1 = run_prep_session(
#     section_ids  = [5, 8],
#     simulate     = True,
#     correct_rate = 0.5,
#     output_dir   = "outputss/scenario_b_iter1"
#     )

#     logger.info("Scenario b complete")

# except Exception as e:
#     logger.exception("ERROR OCCURRED IN DEMO RUN")







# from src.utils.logger import get_logger

# logger = get_logger("demo")

# try:
#     from src.pipeline.run_session import run_prep_session

#     logger.info("Starting Scenario B")


#     result_b3 = run_prep_session(
#         section_ids  = [8],
#         simulate     = True,
#         correct_rate = 0.8,
#         output_dir   = "outputss/scenario_b_iter3"
#     )


#     logger.info("Scenario B — Iteration 2 complete")

# except Exception as e:
#     logger.exception("ERROR OCCURRED IN DEMO RUN")




# from src.utils.logger import get_logger

# logger = get_logger("demo")

# try:
#     from src.pipeline.run_session import run_prep_session

#     logger.info("Starting Scenario B")


#     result_b3 = run_prep_session(
#             section_ids  = [8],
#             simulate     = True,
#             correct_rate = 0.8,
#             output_dir   = "outputss/scenario_b_iter3"
#         )


#     logger.info("Scenario B — Iteration 3 complete")

# except Exception as e:
#     logger.exception("ERROR OCCURRED IN DEMO RUN")





# import glob
# import os
# import json

# from src.utils.logger import get_logger

# logger = get_logger("demo")


# # ================================================================
# # Output file tree
# # ================================================================

# logger.info("Output file tree:")

# for f in sorted(glob.glob("outputss/**/*.json", recursive=True)):
#     size = os.path.getsize(f)
#     logger.info(f"{f} ({size:,} bytes)")


# # ================================================================
# # Preview iter3 KB snapshot
# # ================================================================

# logger.info("KB Snapshot preview (iter3, first session)")

# with open(
#     "outputss/scenario_b_iter3/kb_snapshot.json",
#     "r",
#     encoding="utf-8"
# ) as f:
#     snap = json.load(f)

# first = snap["kb_snapshot"][0]

# logger.info(f"session_id  : {first['session_id']}")
# logger.info(f"section_ids : {first['section_ids']}")

# logger.info(
#     f"score       : "
#     f"{first['correct_count']}/{first['total_q']} "
#     f"({first['score_pct']}%)"
# )

# logger.info(f"questions   : {len(first['questions'])}")

# logger.info("ALL DEMO RUNS COMPLETED SUCCESSFULLY")
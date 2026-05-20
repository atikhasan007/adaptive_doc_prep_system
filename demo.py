


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




from src.utils.logger import get_logger

logger = get_logger("demo")

try:
    from src.pipeline.run_session import run_prep_session

    logger.info("Starting Scenario A")

    result_a = run_prep_session(
        section_ids=[1, 2],
        simulate=True,
        correct_rate=0.5,
        output_dir="outputss/scenario_a"
    )

    logger.info("Scenario A complete")

except Exception as e:
    logger.exception("ERROR OCCURRED IN DEMO RUN")
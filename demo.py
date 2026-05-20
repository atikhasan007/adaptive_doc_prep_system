


# # logger system check 

# from src.utils.logger import get_logger

# logger = get_logger("pdf_processing")

# logger.info("PDF loading started")





from src.utils.logger import get_logger
from src.config.config import get_config

# ================= LOGGER =================
logger = get_logger("demo")

logger.info("System starting...")

# ================= CONFIG =================
config = get_config()

logger.info("Config Loaded Successfully")

logger.info(f"PDF Path: {config['PDF_PATH']}")
logger.info(f"DB Name: {config['MONGODB_DB']}")
logger.info(f"Chroma Path: {config['CHROMA_PERSIST']}")
logger.info(f"MCQ per section: {config['MCQ_PER_SECTION']}")

logger.info("Demo setup completed successfully")
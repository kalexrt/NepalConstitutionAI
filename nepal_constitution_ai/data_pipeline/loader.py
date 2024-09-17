from langchain_community.document_loaders import PyPDFLoader
from nepal_constitution_ai.config.config import settings
from loguru import logger

def load_pdf():
    try:
        logger.info(f"Attempting to load PDF from {settings.FILE_PATH}")
        loader = PyPDFLoader(
            file_path=settings.FILE_PATH,
            extract_images=True
        )
        logger.info("PDF loaded successfully")
        return loader

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred while loading the PDF: {e}")

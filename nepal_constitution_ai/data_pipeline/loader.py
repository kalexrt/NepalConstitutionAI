import os
from loguru import logger
from langchain_community.document_loaders import PyPDFLoader
from nepal_constitution_ai.config.config import settings

def load_pdf(file_path: str) -> list[dict] | None:
    """Loads a PDF file and returns its content as a list of dictionaries, or None if unsuccessful."""
    
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension != '.pdf': # validate pdf file only
        logger.error(f"Invalid file type: {file_extension}. Expected a .pdf file.")
        return None
    
    try:
        logger.info(f"Attempting to load PDF from {file_path}")
        loader = PyPDFLoader(
            file_path=file_path,
            extract_images=False # Images are excluded.
        )
        logger.info("PDF loaded successfully")
        return loader.load()

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")

    except Exception as e: # Catch any other unexpected errors that might occur and log them
        logger.error(f"An error occurred while loading the PDF: {e}")

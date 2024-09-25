import os
from loguru import logger
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str) -> list[dict] | None:
    file_path = file_path
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension != '.pdf':
        logger.error(f"Invalid file type: {file_extension}. Expected a .pdf file.")
        return None
    
    try:
        logger.info(f"Attempting to load PDF from {file_path}")
        loader = PyPDFLoader(
            file_path=file_path,
            extract_images=False
        )
        logger.info("PDF loaded successfully")
        return loader.load()

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred while loading the PDF: {e}")

from langchain_openai import OpenAIEmbeddings
from loguru import logger
from nepal_constitution_ai.config.config import settings

def embed_chunks(chunked_data: list[str]) -> list[list[float]]:
    """Embeds a list of text chunks into vector representations using the OpenAI embeddings model.
    Returns the embedded vectors or None if an error occurs.
    """
    try:
        logger.info("Embedding chunks...")
        model = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)

        embedded_chunks = model.embed_documents(chunked_data)
        logger.info("Chunks embedded successfully.")
        return embedded_chunks
    
    except Exception as e:  # Catch any exception during the embedding process and return none
        logger.error(f"An error occurred while embedding chunks: {e}")  
        return None  
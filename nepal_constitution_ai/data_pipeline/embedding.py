from langchain_community.embeddings import JinaEmbeddings
from loguru import logger
from nepal_constitution_ai.config.config import settings

def embed_chunks(chunked_data: list[str]) -> list[list[float]]:
    """Embeds a list of text chunks into vector representations using the OpenAI embeddings model.
    Returns the embedded vectors or None if an error occurs.
    """
    try:
        logger.info("Embedding chunks...")
        model = JinaEmbeddings(model=settings.JINA_EMBEDDING_MODEL, jina_api_key=settings.JINA_API_KEY)

        embedded_chunks = model.embed_documents(chunked_data)
        logger.info("Chunks embedded successfully.")
        return embedded_chunks
    
    except Exception as e:  # Catch any exception during the embedding process and return none
        logger.error(f"An error occurred while embedding chunks: {e}")  
        raise e
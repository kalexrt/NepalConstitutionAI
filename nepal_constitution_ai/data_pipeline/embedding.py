from langchain_openai import OpenAIEmbeddings
from loguru import logger
from nepal_constitution_ai.config.config import settings

def embed_chunks(chunked_data: list[str]) -> list[list[float]]:
    logger.info("Embedding chunks...")
    model = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)
    embedded_chunks = model.embed_documents(chunked_data)
    logger.info("Chunks embedded successfully.")
    return embedded_chunks
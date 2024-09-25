from langchain_pinecone import PineconeVectorStore

from nepal_constitution_ai.models.openai.openai_model import OpenaiModel
from nepal_constitution_ai.config.config import settings

def get_llm(llm_name: str) -> OpenaiModel:
    """
    Retrieves an OpenAI model based on the given model name. The function checks
    if the provided LLM name matches one of the predefined models (GPT-3.5, GPT-4).

    Args:
        llm_name (str): The name of the desired LLM model.

    Returns:
        OpenaiModel: The selected OpenAI model.

    Raises:
        ValueError: If the provided LLM name is invalid.
    """
    if llm_name.lower() in settings.OPENAI_MODEL:
        llm_model = OpenaiModel(llm_name).model_selection()
    else:
        return ValueError("Wrong llm model selected")

    return llm_model


def get_vector_retriever(vector_db: str, embedding, k: int = 4):
    """
    Retrieves a vector store retriever based on the given vector database name.
    Specifically configured for Pinecone, the function returns a retriever that
    can perform similarity search with the specified number of top results (k).

    Args:
        vector_db (str): The name of the vector database (e.g., 'pinecone').
        embedding (callable): The embedding function used to convert queries into vectors.
        k (int, optional): The number of top similar results to return. Defaults to 4.

    Returns:
        PineconeVectorStore: A configured Pinecone retriever object.

    Raises:
        ValueError: If an unsupported vector database is provided.
    """
    if vector_db.lower() == settings.VECTOR_DB:
        pinecone_index = settings.PINECONE_INDEX

        return PineconeVectorStore(
            index_name=pinecone_index,
            embedding=embedding,
            pinecone_api_key= settings.PINECONE_API_KEY,
            
        ).as_retriever(search_kwargs={"k": k})

    else:
        raise ValueError(f"Unsupported vector database: {vector_db}")
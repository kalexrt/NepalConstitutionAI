from langchain_pinecone import PineconeVectorStore

from nepal_constitution_ai.models.openai.openai_model import OpenaiModel
from nepal_constitution_ai.config.config import settings



def get_llm(llm_name: str) -> OpenaiModel:
    if llm_name.lower() in settings.OPENAI_MODEL:
        llm_model = OpenaiModel(llm_name).model_selection()
    else:
        return ValueError("Wrong llm model selected")

    return llm_model


def get_vector_retriever(vector_db: str, embedding, k: int = 4):
    if vector_db.lower() == settings.VECTOR_DB:
        pinecone_index = settings.PINECONE_INDEX

        return PineconeVectorStore(
            index_name=pinecone_index,
            embedding=embedding,
            pinecone_api_key= settings.PINECONE_API_KEY,
            
        ).as_retriever(search_kwargs={"k": k})

    else:
        raise ValueError(f"Unsupported vector database: {vector_db}")

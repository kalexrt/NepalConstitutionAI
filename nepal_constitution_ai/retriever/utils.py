from langchain_pinecone import PineconeVectorStore

from nepal_constitution_ai.models.openai.openai_model import OpenaiModel
from nepal_constitution_ai.config.config import settings
from nepal_constitution_ai.utils.utils import LLM, VectorDB



def get_llm(llm_name: str) -> OpenaiModel:
    if llm_name.lower() in [LLM.GPT_3_5, LLM.GPT_4o_MINI]:
        llm_model = OpenaiModel(llm_name).model_selection()
    else:
        return ValueError("Wrong llm model selected")

    return llm_model


def get_vector_retriever(vector_db: str, embedding, k: int = 4):
    if vector_db.lower() == VectorDB.PINECONE:
        pinecone_index = settings.PINECONE_INDEX

        return PineconeVectorStore(
            index_name=pinecone_index,
            embedding=embedding,
            pinecone_api_key= settings.PINECONE_API_KEY,
            
        ).as_retriever(search_kwargs={"k": k})

    else:
        raise ValueError(f"Unsupported vector database: {vector_db}")

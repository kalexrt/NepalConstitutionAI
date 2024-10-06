from langchain_core.messages.ai import AIMessage
from langchain_community.embeddings import JinaEmbeddings
from loguru import logger
from fastapi import HTTPException
import json

from nepal_constitution_ai.chat.schemas import ChatResponse, ChatHistory
from nepal_constitution_ai.config.config import settings
from nepal_constitution_ai.retriever.chains import (
    RetrieverChain,
    rewrite_query,
    setup_conversation_chain,
)
from nepal_constitution_ai.agent.agent import setup_agent
from nepal_constitution_ai.retriever.utils import (
    get_llm,
    get_vector_retriever,
    format_chat_history
)

class Retriever:
    def __init__(
        self,
        llm: str,
        chat_history: ChatHistory,
        vector_db: str,
        mode: str = "retriever"
    ) -> None:
        self.embedding = JinaEmbeddings(model=settings.JINA_EMBEDDING_MODEL, jina_api_key=settings.JINA_API_KEY)
        self.chat_history = chat_history
        self.llm_model = get_llm(llm)
        self.base_retriever = get_vector_retriever(
            vector_db=vector_db, embedding=self.embedding
        )
        self.mode = mode
        self.retriever_chain = RetrieverChain(
            retriever=self.base_retriever,
            llm_model=self.llm_model,
        ).get_chain()

        self.conv_chain = setup_conversation_chain(
            llm_model=self.llm_model,
        )
        self.agent = setup_agent(
            retriever_chain=self.retriever_chain,
            conv_chain=self.conv_chain,
            llm_model=self.llm_model,
        )

    # invoke function for the retriever
    def invoke(self, query: str):
        try:
            if len(self.chat_history.get_messages()) > 0:
                new_query = rewrite_query(
                    query=query, llm_model=self.llm_model, history=self.chat_history
                )
            else:
                new_query = f"""{{
                    "user_question": {query},
                    "reformulated_question": ""
                }}
                """

            new_query = new_query.strip()
            new_query = new_query.replace("\n", "")
            if new_query[-2] == ",":
                new_query = new_query[:-2] + "}"

            new_query = json.loads(new_query)
            
            chat_history_formatted = format_chat_history(
                self.chat_history.get_messages()[:-1]
            )
            inputs = {
                "user_question": new_query["user_question"],
                "reformulated_question": new_query["reformulated_question"] ,
                "chat_history": chat_history_formatted,
            }
            if self.mode == "evaluation":
                result = self.retriever_chain.invoke(
                    {"input": new_query}
                )
                return result
            
            result = self.agent.invoke(
                    {"input": inputs}
                )
            output = result["output"]["answer"]
            if isinstance(output, AIMessage):
                if isinstance(output.content, str):
                    return ChatResponse(message=output.content)
            return ChatResponse(message="")

        except HTTPException as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise HTTPException(
                detail=f"An error occurred while processing your query: {str(e)}",
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise e
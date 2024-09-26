from langchain_core.messages.ai import AIMessage
from langchain_openai import OpenAIEmbeddings
from loguru import logger
from fastapi import HTTPException

from nepal_constitution_ai.utils.utils import ChatResponse
from nepal_constitution_ai.utils.utils import ChatHistory
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
)

class Retriever:
    def __init__(
        self,
        llm: str,
        chat_history: ChatHistory,
        vector_db: str,
    ) -> None:
        self.embedding = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)
        self.chat_history = chat_history
        self.llm_model = get_llm(llm)
        self.base_retriever = get_vector_retriever(
            vector_db=vector_db, embedding=self.embedding
        )

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
                new_query = query

            result = self.agent.invoke(
                {"input": new_query}
            )
            output = result["output"]

            if isinstance(output, AIMessage):
                if isinstance(output.content, str):
                    return ChatResponse(message=output.content)
                else:
                    return ChatResponse(message="")
            else:
                answer_op = output["answer"]
                answer = answer_op.get("answer", "")


                result = ChatResponse(message=answer)
                return result

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your query: {str(e)}",
            )

print(Retriever(llm="gpt-3.5-turbo",chat_history=ChatHistory(), vector_db="pinecone").invoke("who is the current president of nepal"))
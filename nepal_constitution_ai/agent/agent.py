from nepal_constitution_ai.agent.utils import create_agent
from nepal_constitution_ai.retriever.chains import RetrieverChain
from nepal_constitution_ai.models.openai.openai_model import OpenaiModel
from nepal_constitution_ai.models.groq.groq_model import GroqModel
from langchain.chains import LLMChain
from typing import Union

from langchain.tools import Tool

def setup_agent(
    retriever_chain: RetrieverChain,
    conv_chain: LLMChain,
    llm_model: Union[OpenaiModel, GroqModel],
):
    tools = [
        Tool(
            name="Vector Search",
            func=lambda query: retriever_chain.invoke(query),
            description=f"Useful for answering any legal questions related to nepal, its laws, its punishments etc",
            return_direct=True,
        ),
        Tool(
            name="Conversation",
            func=lambda query: conv_chain.invoke({"input": query}),
            description="Useful for greetings ONLY",
            return_direct=True,
        ),
    ]

    return create_agent(
        llm_model,
        tools
    )
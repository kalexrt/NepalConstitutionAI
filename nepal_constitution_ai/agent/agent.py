from nepal_constitution_ai.agent.utils import create_agent
from langchain.tools import Tool

def setup_agent(
    retriever_chain,
    conv_chain,
    llm_model,
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
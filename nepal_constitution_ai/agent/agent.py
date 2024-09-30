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
            description=f"""Useful for answering questions by a bot named Nepal Constitution AI that is described 
            as a helpful AI assistant who can answer questions about 
            the constitution or law of Nepal and also relate the other 
            questions and generate smart answers as per the constitution or law of Nepal. 
            Also useful if the user question can be answered by the context provided by Vector Search where
            the context refers to the laws and regulation articles and schedules 
            mentioned in the Constitution""",
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
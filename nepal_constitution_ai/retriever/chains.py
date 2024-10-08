from langchain.schema.runnable import RunnableLambda
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
import json
from langchain_core.runnables import chain

from nepal_constitution_ai.prompts.prompts import HUMAN_PROMPT, SYSTEM_PROMPT, CONTEXTUALIZE_Q_SYSTEM_PROMPT, CONVERSATION_PROMPT


@chain
def format_docs_with_id(docs):
    """
    Format a list of documents by extracting page content and metadata.
    Each document is formatted with "Content" and "Metadata" sections.
    
    Args:
        docs (list): A list of documents to be formatted.

    Returns:
        str: A string representation of the formatted documents.
    """
    if isinstance(docs, list):
        # Joining formatted strings for each document, with page content and metadata
        return "\n\n".join(
            f"Content: {doc.page_content}\nMetadata: {doc.metadata}"
            for doc in docs
        )
    return "Unexpected document type"

def setup_conversation_chain(llm_model):
    conversation_chain_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                CONVERSATION_PROMPT,
            ),
            ("human", "{input}"),
        ]
    )

    return conversation_chain_prompt | llm_model | RunnableLambda(
                lambda x: {
                    "answer": x,
                })

class RetrieverChain:
    """
    A class that integrates a document retriever and an LLM model to retrieve 
    and format documents and generate an answer based on user input.
    """
    def __init__(
        self,
        retriever,
        llm_model
    ) -> None:
        self.retriever = retriever
        self.llm_model = llm_model


        # Setting the document formatting function
        self.format_docs = format_docs_with_id

        # Defining the prompt template with system and human message templates
        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessagePromptTemplate.from_template(HUMAN_PROMPT),
            ],
            input_variables=["question", "chat_history", "context"],
        )

    def retrieve_and_format(self, inputs):
        """
        Retrieves documents based on the query and formats them.

        Args:
            query (str): The user input query.

        Returns:
            dict: A dictionary containing formatted documents and the original documents.
        """
        if isinstance(inputs, dict):
            docs = self.retriever.invoke(inputs["input"])
        else:
            inputs = json.loads(inputs)
            docs = self.retriever.invoke(inputs["reformulated_question"])
        
        formatted_docs = self.format_docs.invoke(docs)

        return {"context": formatted_docs, "question": inputs, "chat_history": inputs["chat_history"], "orig_context": docs}

    def generate_answer(self, inputs):
        """
        Generates an answer using the LLM based on the formatted input.

        Args:
            inputs (dict): Contains the formatted documents and the original question.

        Returns:
            dict: Contains the context, generated answer, and original documents.
        """

        query = inputs["question"]

        if not isinstance(query, dict):
            query = json.loads(query)

        inputs["question"] = query["user_question"]
        formatted_prompt = self.prompt.format(**inputs)
        answer = self.llm_model.invoke(formatted_prompt)

        return {
            "context": inputs["context"],
            "answer": answer,
            "orig_docs": inputs["orig_context"],
        }

    def get_chain(self):
        """
        Creates a chain of operations that retrieves, formats, and generates an answer.

        Returns:
            Callable: The chain of operations as a callable object.
        """
        rag_chain = (
            RunnableLambda(self.retrieve_and_format)
            | self.generate_answer
            | RunnableLambda(
                lambda x: {
                    "context": x["context"],
                    "answer": x["answer"],
                    "orig_context": x["orig_docs"],
                }
            )
        )

        return rag_chain


def rewrite_query(query, llm_model, history):
    """
    Reformulates the user's query by incorporating chat history for better context.

    Args:
        query (str): The original user query.
        llm_model (object): The LLM model to generate the reformulated query.
        history (object): The chat history for context.

    Returns:
        str: The reformulated query as text content.
    """

    # Create a prompt to reformulate the query using the chat history
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            (
                "human",
                "{user_question}",
            ),
        ]
    )

    new_query_chain = contextualize_q_prompt | llm_model
    # Invoke the LLM with the user question and chat history
    res = new_query_chain.invoke(
        {"user_question": query, "chat_history": history.get_messages()[:-1]}
    )

    return res.content
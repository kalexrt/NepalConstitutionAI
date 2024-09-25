from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.runnables import chain

from nepal_constitution_ai.prompts.prompts import HUMAN_PROMPT, SYSTEM_PROMPT, contextualize_q_system_prompt


@chain
def format_docs_with_id(docs):
    if isinstance(docs, list):
        return "\n\n".join(
            f"Content: {doc.page_content}\nMetadata: {doc.metadata}"
            for doc in docs
        )
    return "Unexpected document type"


class RetrieverChain:
    def __init__(
        self,
        retriever,
        llm_model
    ) -> None:
        self.retriever = retriever
        self.llm_model = llm_model

        self.output_parser = StructuredOutputParser.from_response_schemas(
            [
                ResponseSchema(
                    name="answer",
                    description="The answer to the user question, with the source",
                ),
            ]
        )

        format_instructions = self.output_parser.get_format_instructions()

        self.format_docs = format_docs_with_id

        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessagePromptTemplate.from_template(HUMAN_PROMPT),
            ],
            input_variables=["question", "context"],
            partial_variables={"format_instructions": format_instructions},
        )

    def retrieve_and_format(self, query):
        docs = self.retriever.invoke(query)
        formatted_docs = self.format_docs.invoke(docs)

        return {"context": formatted_docs, "question": query, "orig_context": docs}

    def generate_answer(self, inputs):
        formatted_prompt = self.prompt.format(**inputs)
        answer = self.llm_model.invoke(formatted_prompt)
        answer = self.output_parser.invoke(answer)

        return {
            "context": inputs["context"],
            "answer": answer,
            "orig_docs": inputs["orig_context"],
        }

    def get_chain(self):
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
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            (
                "human",
                "Reformulate the given question using the chat history: {user_question}",
            ),
        ]
    )

    new_query_chain = contextualize_q_prompt | llm_model
    res = new_query_chain.invoke(
        {"user_question": query, "chat_history": history.get_messages()}
    )

    return res.content


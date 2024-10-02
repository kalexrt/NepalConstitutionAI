from nepal_constitution_ai.config.config import settings
from nepal_constitution_ai.chat.schemas import ChatHistory
from nepal_constitution_ai.evaluation.data import eval_data
from nepal_constitution_ai.retriever.retriever_base import Retriever

chat_history = ChatHistory()
print(eval_data)
retriever = Retriever(
        llm=settings.OPENAI_MODEL,
        vector_db=settings.VECTOR_DB,
        chat_history=chat_history,
    )

for i, question in enumerate(eval_data["question"]):
    response = retriever.invoke(query = question)
    eval_data['answer'].append(response)

for i in range(5):
    print(eval_data['answer'][i])


from langchain_openai import ChatOpenAI

from nepal_constitution_ai.config.config import settings



class OpenaiModel:
    def __init__(self, model_name=settings.OPENAI_MODEL) -> None:
        self.model_name = model_name
        self.temperature = 0.1

    def model_selection(self):
        llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            api_key=settings.OPENAI_API_KEY,
        )
        return llm

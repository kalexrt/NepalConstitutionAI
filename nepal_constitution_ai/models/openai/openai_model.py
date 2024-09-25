from langchain_openai import ChatOpenAI

from nepal_constitution_ai.config.config import settings
from nepal_constitution_ai.utils.utils import LLM, LLM_MAP


class OpenaiModel:
    def __init__(self, model_name=LLM.GPT_3_5):
        self.model_name = LLM_MAP.get(model_name)
        self.temperature = 0.1

    def model_selection(self):
        llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            api_key=settings.OPENAI_API_KEY,
        )
        return llm

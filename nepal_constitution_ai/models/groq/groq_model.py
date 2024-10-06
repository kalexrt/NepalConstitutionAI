from langchain_groq import ChatGroq
from nepal_constitution_ai.config.config import settings



class GroqModel:
    def __init__(self, model_name=settings.GROQ_MODEL) -> None:
        self.model_name = model_name
        self.temperature = 0.1

    def model_selection(self):
        llm = ChatGroq(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=settings.GROQ_API_KEY
                        )
        return llm

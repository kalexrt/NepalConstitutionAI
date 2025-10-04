from langchain_google_genai import ChatGoogleGenerativeAI

from nepal_constitution_ai.config.config import settings


class GeminiModel:
    def __init__(self, model_name=settings.GEMINI_MODEL) -> None:
        self.model_name = model_name
        self.temperature = 0.1

    def model_selection(self, key_num):
        if key_num == "A":
            return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=settings.GEMINI_API_KEY_A,
        )
        else:
            return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=settings.GEMINI_API_KEY_B,
        )
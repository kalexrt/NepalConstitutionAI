from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    LANGSMITH_API_KEY: str
    PINECONE_API_KEY: str
    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str = ""
    OPENAI_MODEL: str = ""
    PINECONE_INDEX: str = ""
    FILE_PATH: str = "./data/refined_nepal_constitution_ai.pdf"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

__all__ = ["settings"]
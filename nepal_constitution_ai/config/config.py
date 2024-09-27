import os
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
    EMBEDDING_MODEL: str
    EMBEDDING_DIM: str
    OPENAI_MODEL: str 
    VECTOR_DB: str 
    PINECONE_INDEX: str
    PINECONE_CLOUD: str 
    PINECONE_REGION: str
    FILE_PATH: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
os.environ["LANGCHAIN_TRACING_V2"]="true" # enables the tracing
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]=settings.LANGSMITH_API_KEY
os.environ["LANGCHAIN_PROJECT"]="RAG-FINAL_PROJECT"
__all__ = ["settings"]